"""Fast access to canonical processed detection data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import numpy as np

from medimg.loader.contracts import SampleTransform


class DetectionDataset:
    """Read prepared NPY images and canonical annotations without raw decoding."""

    def __init__(
        self,
        dataset_dir: str | Path,
        split: str,
        transform: SampleTransform | None = None,
    ):
        self.dataset_dir = Path(dataset_dir).expanduser().resolve()
        self.split = split
        self.transform = transform
        manifest_path = self.dataset_dir / "dataset_manifest.json"
        if not manifest_path.is_file():
            raise FileNotFoundError(f"Processed dataset manifest not found: {manifest_path}")
        self.manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if self.manifest.get("schema_version") != 1:
            raise ValueError(f"Unsupported processed dataset schema in {manifest_path}")
        if split not in self.manifest.get("image_counts", {}):
            available = ", ".join(sorted(self.manifest.get("image_counts", {})))
            raise ValueError(f"Unknown split {split!r}; available splits: {available}")

        records_path = self.dataset_dir / split / "annotations.jsonl"
        if not records_path.is_file():
            raise FileNotFoundError(f"Processed split manifest not found: {records_path}")
        with records_path.open(encoding="utf-8") as records_file:
            self.records = [json.loads(line) for line in records_file if line.strip()]
        expected = self.manifest["image_counts"][split]
        if len(self.records) != expected:
            raise ValueError(
                f"Processed split {split!r} has {len(self.records)} records; expected {expected}"
            )

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, index: int) -> dict[str, Any]:
        record = self.records[index]
        image_path = (self.dataset_dir / self.split / record["image"]).resolve()
        split_root = (self.dataset_dir / self.split).resolve()
        if not image_path.is_relative_to(split_root):
            raise ValueError(f"Processed image path escapes the dataset directory: {record['image']!r}")
        if not image_path.is_file():
            raise FileNotFoundError(f"Processed image missing for {record['sample_id']}: {image_path}")
        image = np.load(image_path, mmap_mode="r", allow_pickle=False)
        if image.dtype != np.uint8 or image.ndim != 2:
            raise ValueError(f"Expected grayscale uint8 NPY image; got {image.dtype} {image.shape}")
        if image.shape != (record["height"], record["width"]):
            raise ValueError(
                f"Image dimensions mismatch for {record['sample_id']}: "
                f"manifest={(record['height'], record['width'])}, array={image.shape}"
            )
        boxes = np.asarray(record["boxes"], dtype=np.float32).reshape((-1, 4))
        labels = np.asarray(record["labels"], dtype=np.int64)
        if len(boxes) != len(labels):
            raise ValueError(f"Box/label count mismatch for {record['sample_id']}")
        if len(labels) and (
            np.any(labels < 0) or np.any(labels >= len(self.manifest["class_names"]))
        ):
            raise ValueError(f"Out-of-range class label for {record['sample_id']}")
        if len(boxes):
            x_min, y_min, x_max, y_max = boxes.T
            invalid = (
                ~np.isfinite(boxes).all(axis=1)
                | (x_min < 0)
                | (y_min < 0)
                | (x_max <= x_min)
                | (y_max <= y_min)
                | (x_max > record["width"])
                | (y_max > record["height"])
            )
            if np.any(invalid):
                raise ValueError(f"Invalid box coordinates for {record['sample_id']}")
        target = {
            "boxes": boxes,
            "labels": labels,
            "image_id": record["sample_id"],
        }
        if self.transform is not None:
            image, target = self.transform(image, target)
        return {
            "image": image,
            "target": target,
            "metadata": {
                "sample_id": record["sample_id"],
                "source_file": record["source_file"],
                "width": record["width"],
                "height": record["height"],
            },
        }


def detection_collate(batch: list[dict[str, Any]]) -> tuple[list[Any], list[Any], list[dict[str, Any]]]:
    """Collate variable-sized detection samples for a torch DataLoader."""
    return (
        [sample["image"] for sample in batch],
        [sample["target"] for sample in batch],
        [sample["metadata"] for sample in batch],
    )
