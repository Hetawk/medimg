from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZipFile

import numpy as np
from PIL import Image
import pytest

from medimg.adapters.chestxdet10 import ChestXDet10Adapter
from medimg.loader import DetectionDataset, detection_collate
from medimg.cli import main


def _write_source_split(root: Path, split: str, records: list[dict]) -> None:
    (root / "annotations").mkdir(parents=True, exist_ok=True)
    (root / "annotations" / f"{split}.json").write_text(
        json.dumps(records), encoding="utf-8"
    )
    with ZipFile(root / f"{split}_data.zip", "w") as archive:
        for record in records:
            image = Image.fromarray(np.full((12, 16), 127, dtype=np.uint8), mode="L")
            from io import BytesIO

            buffer = BytesIO()
            image.save(buffer, format="PNG")
            archive.writestr(f"{split}-folder/{record['file_name']}", buffer.getvalue())


def _make_source(root: Path) -> Path:
    _write_source_split(
        root,
        "train",
        [
            {
                "file_name": "image-a.png",
                "syms": ["Nodule"],
                "boxes": [[1, 2, 10, 11]],
            },
            {"file_name": "image-b.png", "syms": [], "boxes": []},
        ],
    )
    _write_source_split(
        root,
        "test",
        [{"file_name": "image-c.png", "syms": ["Mass"], "boxes": [[0, 0, 16, 12]]}],
    )
    return root


def test_prepare_materializes_canonical_data_and_reuses_cache(tmp_path: Path) -> None:
    raw_root = _make_source(tmp_path / "raw")
    processed_root = tmp_path / "processed"
    adapter = ChestXDet10Adapter(raw_root)

    first = adapter.prepare(processed_root)
    second = adapter.prepare(processed_root)

    assert first.reused is False
    assert second.reused is True
    assert first.dataset_dir == second.dataset_dir
    assert first.image_counts == {"train": 2, "test": 1}

    dataset = DetectionDataset(first.dataset_dir, "train")
    positive = dataset[0]
    negative = dataset[1]
    assert positive["image"].shape == (12, 16)
    assert positive["image"].dtype == np.uint8
    assert positive["target"]["boxes"].tolist() == [[1.0, 2.0, 10.0, 11.0]]
    assert positive["target"]["labels"].tolist() == [8]
    assert negative["target"]["boxes"].shape == (0, 4)
    assert negative["target"]["labels"].shape == (0,)

    images, targets, metadata = detection_collate([positive, negative])
    assert len(images) == len(targets) == len(metadata) == 2


def test_prepare_rejects_annotation_box_outside_image(tmp_path: Path) -> None:
    raw_root = _make_source(tmp_path / "raw")
    train_path = raw_root / "annotations" / "train.json"
    records = json.loads(train_path.read_text(encoding="utf-8"))
    records[0]["boxes"] = [[1, 2, 17, 11]]
    train_path.write_text(json.dumps(records), encoding="utf-8")

    with pytest.raises(ValueError, match="exceeds image bounds"):
        ChestXDet10Adapter(raw_root).prepare(tmp_path / "processed")
    assert not list((tmp_path / "processed" / "chestxdet10").glob("*.staging-*"))


def test_processed_loader_rejects_path_traversal(tmp_path: Path) -> None:
    raw_root = _make_source(tmp_path / "raw")
    result = ChestXDet10Adapter(raw_root).prepare(tmp_path / "processed")
    records_path = result.dataset_dir / "train" / "annotations.jsonl"
    records = [
        json.loads(line)
        for line in records_path.read_text(encoding="utf-8").splitlines()
    ]
    records[0]["image"] = "../../outside.npy"
    records_path.write_text(
        "\n".join(json.dumps(record) for record in records) + "\n",
        encoding="utf-8",
    )

    dataset = DetectionDataset(result.dataset_dir, "train")
    with pytest.raises(ValueError, match="escapes"):
        dataset[0]


def test_prepare_detects_duplicate_archive_basenames(tmp_path: Path) -> None:
    raw_root = _make_source(tmp_path / "raw")
    train_archive = raw_root / "train_data.zip"
    with ZipFile(train_archive, "a") as archive:
        image = Image.fromarray(np.zeros((12, 16), dtype=np.uint8))
        from io import BytesIO

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        archive.writestr("duplicate/image-a.png", buffer.getvalue())

    with pytest.raises(ValueError, match="Ambiguous image basename"):
        ChestXDet10Adapter(raw_root).prepare(tmp_path / "processed")


def test_cli_prepare_and_inspect_round_trip(tmp_path: Path, capsys) -> None:
    raw_root = _make_source(tmp_path / "raw")
    processed_root = tmp_path / "processed"
    archive_before = {
        split: (raw_root / f"{split}_data.zip").read_bytes()
        for split in ("train", "test")
    }

    assert main(
        [
            "prepare",
            "-d",
            "chestxdet10",
            "--raw",
            str(raw_root),
            "--out",
            str(processed_root),
        ]
    ) == 0
    prepare_output = capsys.readouterr().out
    assert "Prepared chestxdet10:" in prepare_output
    assert "Raw archives were read but not modified." in prepare_output
    assert all(
        archive_before[split] == (raw_root / f"{split}_data.zip").read_bytes()
        for split in ("train", "test")
    )

    processed_dir = next((processed_root / "chestxdet10").iterdir())
    assert main(
        [
            "inspect",
            "--data",
            str(processed_dir),
            "-s",
            "train",
            "-n",
            "1",
        ]
    ) == 0
    inspection = json.loads(capsys.readouterr().out)
    assert inspection["samples"] == 2
    assert inspection["boxes"] == 1
    assert inspection["empty_images"] == 1
    assert len(inspection["sample_examples"]) == 1
