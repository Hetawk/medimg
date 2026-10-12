"""Command-line entry point for dataset preparation and inspection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from medimg.loader import DetectionDataset
from medimg.loader.builtin import register_builtin_datasets
from medimg.registry.datasets import create_dataset, list_datasets


register_builtin_datasets()


def _default_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="medimg",
        description="Prepare and inspect reusable medical-imaging datasets.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    datasets = commands.add_parser("datasets", help="List registered datasets.")
    datasets.add_argument("action", choices=("list",))

    prepare = commands.add_parser(
        "prepare",
        help="Materialize a raw dataset into the processed-data cache.",
    )
    prepare.add_argument("-d", "--dataset", required=True, help="Registered dataset name.")
    prepare.add_argument(
        "-r",
        "--raw",
        type=Path,
        required=True,
        help="Read-only root containing the original dataset files.",
    )
    prepare.add_argument(
        "-o",
        "--out",
        type=Path,
        default=_default_project_root() / "processed_data",
        help="Cache root; defaults to the ignored project processed_data/ directory.",
    )
    prepare.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Rebuild the matching prepared artifact from raw sources.",
    )

    inspect = commands.add_parser(
        "inspect",
        help="Validate and summarize a processed dataset split.",
    )
    inspect.add_argument("-p", "--data", type=Path, required=True)
    inspect.add_argument("-s", "--split", required=True)
    inspect.add_argument("-n", "--samples", type=int, default=3)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "datasets":
        for dataset in list_datasets():
            print(f"{dataset.name}\t{dataset.task}\t{dataset.description}")
        return 0

    if args.command == "prepare":
        adapter = create_dataset(args.dataset, raw_dir=args.raw)
        result = adapter.prepare(
            args.out,
            force=args.force,
            progress=lambda split, current, total: print(
                f"\rPreparing {split}: {current}/{total}",
                end="\n" if current == total else "",
                flush=True,
            ),
        )
        status = "Reused" if result.reused else "Prepared"
        print(f"{status} {adapter.metadata.name}: {result.dataset_dir}")
        print(json.dumps(result.image_counts, sort_keys=True))
        print("Raw archives were read but not modified.")
        return 0

    if args.command == "inspect":
        if args.samples < 0:
            raise ValueError("--samples must be non-negative")
        dataset = DetectionDataset(args.data, args.split)
        class_counts = {name: 0 for name in dataset.manifest["class_names"]}
        box_count = 0
        negative_count = 0
        sample_examples = []
        for index in range(len(dataset)):
            sample = dataset[index]
            labels = sample["target"]["labels"]
            if len(labels) == 0:
                negative_count += 1
            box_count += len(labels)
            for label in labels:
                class_counts[dataset.manifest["class_names"][int(label)]] += 1
            if index < args.samples:
                sample_examples.append(
                    {
                        "sample_id": sample["metadata"]["sample_id"],
                        "image_shape": list(sample["image"].shape),
                        "boxes": len(sample["target"]["boxes"]),
                    }
                )
        summary = {
            "dataset": dataset.manifest["dataset"],
            "split": args.split,
            "samples": len(dataset),
            "boxes": box_count,
            "empty_images": negative_count,
            "class_box_counts": class_counts,
            "sample_examples": sample_examples,
        }
        print(json.dumps(summary, indent=2))
        return 0

    raise AssertionError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
