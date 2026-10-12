"""ChestX-Det10 raw archive adapter and processed-data materializer."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Callable
from zipfile import BadZipFile, ZipFile

import numpy as np
from PIL import Image, UnidentifiedImageError

from medimg.loader.contracts import DatasetMetadata, PreparationResult


DATASET_METADATA = DatasetMetadata(
    name="chestxdet10",
    task="detection",
    class_names=(
        "Atelectasis",
        "Calcification",
        "Consolidation",
        "Effusion",
        "Emphysema",
        "Fibrosis",
        "Fracture",
        "Mass",
        "Nodule",
        "Pneumothorax",
    ),
    description="Chest X-ray bounding-box detection across ten findings.",
)
SCHEMA_VERSION = 1
PREPROCESSING = {
    "format": "npy",
    "dtype": "uint8",
    "pixel_mode": "L",
    "resize": None,
    "normalization": None,
}


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_fingerprint(raw_dir: Path) -> tuple[str, dict[str, Any]]:
    source_info: dict[str, Any] = {"annotations": {}, "archives": {}}
    for split in ("train", "test"):
        annotation_path = raw_dir / "annotations" / f"{split}.json"
        archive_path = raw_dir / f"{split}_data.zip"
        for path in (annotation_path, archive_path):
            if not path.is_file():
                raise FileNotFoundError(f"Required ChestX-Det10 source file not found: {path}")
        source_info["annotations"][split] = {
            "path": str(annotation_path.relative_to(raw_dir)),
            "sha256": _sha256_file(annotation_path),
        }
        stat = archive_path.stat()
        source_info["archives"][split] = {
            "path": str(archive_path.relative_to(raw_dir)),
            "size_bytes": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
        }
    fingerprint_input = {
        "schema_version": SCHEMA_VERSION,
        "preprocessing": PREPROCESSING,
        "source": source_info,
    }
    encoded = json.dumps(fingerprint_input, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()[:16], source_info


def _read_annotations(path: Path, class_to_id: dict[str, int]) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid annotation JSON in {path}: {exc}") from exc
    if not isinstance(payload, list):
        raise ValueError(f"Expected an annotation list in {path}")

    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ValueError(f"{path}: record {index} is not an object")
        file_name = item.get("file_name")
        syms = item.get("syms")
        boxes = item.get("boxes")
        if not isinstance(file_name, str) or not file_name:
            raise ValueError(f"{path}: record {index} has no valid file_name")
        if file_name in seen:
            raise ValueError(f"{path}: duplicate file_name {file_name!r}")
        seen.add(file_name)
        if not isinstance(syms, list) or not isinstance(boxes, list) or len(syms) != len(boxes):
            raise ValueError(f"{path}: record {file_name!r} must have equally sized syms and boxes lists")

        labels: list[int] = []
        checked_boxes: list[list[float]] = []
        for category, box in zip(syms, boxes):
            if not isinstance(category, str) or category not in class_to_id:
                raise ValueError(f"{path}: unknown class {category!r} in {file_name!r}")
            if not isinstance(box, list) or len(box) != 4:
                raise ValueError(f"{path}: invalid xyxy box in {file_name!r}: {box!r}")
            try:
                coordinates = [float(value) for value in box]
            except (TypeError, ValueError) as exc:
                raise ValueError(f"{path}: non-numeric box in {file_name!r}: {box!r}") from exc
            if not np.isfinite(coordinates).all():
                raise ValueError(f"{path}: non-finite box in {file_name!r}: {box!r}")
            x_min, y_min, x_max, y_max = coordinates
            if x_min < 0 or y_min < 0 or x_max <= x_min or y_max <= y_min:
                raise ValueError(f"{path}: invalid positive-area xyxy box in {file_name!r}: {box!r}")
            checked_boxes.append(coordinates)
            labels.append(class_to_id[category])
        records.append({"file_name": file_name, "boxes": checked_boxes, "labels": labels})
    return records


def _index_archive(archive: ZipFile, archive_path: Path) -> dict[str, str]:
    members: dict[str, str] = {}
    supported_extensions = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}
    for member in archive.namelist():
        if member.endswith("/"):
            continue
        basename = Path(member).name
        if basename.startswith(".") or Path(basename).suffix.lower() not in supported_extensions:
            continue
        if basename in members:
            raise ValueError(
                f"Ambiguous image basename {basename!r} in {archive_path}: "
                f"{members[basename]!r} and {member!r}"
            )
        members[basename] = member
    return members


def _materialize_split(
    *,
    split: str,
    records: list[dict[str, Any]],
    archive: ZipFile,
    members: dict[str, str],
    destination: Path,
    progress: Callable[[str, int, int], None] | None = None,
) -> int:
    split_dir = destination / split
    image_dir = split_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = split_dir / "annotations.jsonl"
    written = 0
    referenced: set[str] = set()
    try:
        with manifest_path.open("w", encoding="utf-8") as manifest:
            for record in records:
                file_name = record["file_name"]
                basename = Path(file_name).name
                if basename not in members:
                    raise FileNotFoundError(
                        f"{split}: annotation image {file_name!r} not present in source archive"
                    )
                if basename in referenced:
                    raise ValueError(f"{split}: multiple annotation records resolve to {basename!r}")
                referenced.add(basename)

                relative_image_path = Path("images") / f"{written:06d}.npy"
                output_path = split_dir / relative_image_path
                try:
                    with archive.open(members[basename], "r") as image_file:
                        with Image.open(image_file) as image:
                            image = image.convert(PREPROCESSING["pixel_mode"])
                            width, height = image.size
                            image_array = np.asarray(image, dtype=np.uint8)
                except (BadZipFile, OSError, UnidentifiedImageError) as exc:
                    raise ValueError(f"Could not decode {split} image {file_name!r}: {exc}") from exc

                if image_array.ndim != 2 or width < 1 or height < 1:
                    raise ValueError(f"Unexpected decoded image shape for {file_name!r}: {image_array.shape}")
                boxes = record["boxes"]
                for box in boxes:
                    x_min, y_min, x_max, y_max = box
                    if x_max > width or y_max > height:
                        raise ValueError(
                            f"{split}: box {box!r} exceeds image bounds "
                            f"{width}x{height} for {file_name!r}"
                        )
                np.save(output_path, image_array, allow_pickle=False)
                output_record = {
                    "sample_id": f"{split}-{written:06d}",
                    "source_file": file_name,
                    "image": relative_image_path.as_posix(),
                    "width": width,
                    "height": height,
                    "boxes": boxes,
                    "labels": record["labels"],
                }
                manifest.write(json.dumps(output_record, separators=(",", ":")) + "\n")
                written += 1
                if progress is not None:
                    progress(split, written, len(records))
    except Exception:
        manifest_path.unlink(missing_ok=True)
        raise

    unused = set(members) - referenced
    if unused:
        raise ValueError(
            f"{split}: {len(unused)} archive images have no annotation records "
            f"(example: {min(unused)!r})"
        )
    return written


class ChestXDet10Adapter:
    """Convert ChestX-Det10 ZIP/JSON sources into reusable NPY/JSONL artifacts."""

    metadata = DATASET_METADATA

    def __init__(self, raw_dir: str | Path):
        self.raw_dir = Path(raw_dir).expanduser().resolve()

    def prepare(
        self,
        out_dir: Path,
        *,
        force: bool = False,
        progress: Callable[[str, int, int], None] | None = None,
    ) -> PreparationResult:
        out_dir = Path(out_dir).expanduser().resolve()
        cache_key, source_info = _source_fingerprint(self.raw_dir)
        final_dir = out_dir / self.metadata.name / cache_key
        if final_dir.exists() and not force:
            manifest_path = final_dir / "dataset_manifest.json"
            if not manifest_path.is_file():
                raise FileExistsError(
                    f"Incomplete processed dataset exists at {final_dir}; rerun with --force to rebuild"
                )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if manifest.get("source_fingerprint") != cache_key:
                raise ValueError(f"Processed dataset fingerprint mismatch in {manifest_path}")
            return PreparationResult(
                dataset_dir=final_dir,
                reused=True,
                image_counts=manifest["image_counts"],
            )

        final_dir.parent.mkdir(parents=True, exist_ok=True)
        staging_dir = Path(
            tempfile.mkdtemp(prefix=f".{cache_key}.staging-", dir=final_dir.parent)
        )
        counts: dict[str, int] = {}
        class_to_id = {name: index for index, name in enumerate(self.metadata.class_names)}
        try:
            for split in ("train", "test"):
                annotation_path = self.raw_dir / "annotations" / f"{split}.json"
                archive_path = self.raw_dir / f"{split}_data.zip"
                records = _read_annotations(annotation_path, class_to_id)
                try:
                    with ZipFile(archive_path) as archive:
                        members = _index_archive(archive, archive_path)
                        counts[split] = _materialize_split(
                            split=split,
                            records=records,
                            archive=archive,
                            members=members,
                            destination=staging_dir,
                            progress=progress,
                        )
                except BadZipFile as exc:
                    raise ValueError(f"Invalid ZIP archive: {archive_path}") from exc

            manifest = {
                "schema_version": SCHEMA_VERSION,
                "dataset": self.metadata.name,
                "task": self.metadata.task,
                "class_names": list(self.metadata.class_names),
                "class_id_convention": "zero-based foreground labels; no background label",
                "image_counts": counts,
                "preprocessing": PREPROCESSING,
                "source_fingerprint": cache_key,
                "source_fingerprint_inputs": source_info,
            }
            (staging_dir / "dataset_manifest.json").write_text(
                json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            if final_dir.exists():
                if not force:
                    raise FileExistsError(f"Processed dataset already exists: {final_dir}")
                shutil.rmtree(final_dir)
            os.replace(staging_dir, final_dir)
        except Exception:
            if staging_dir.exists():
                shutil.rmtree(staging_dir)
            raise

        return PreparationResult(dataset_dir=final_dir, reused=False, image_counts=counts)
