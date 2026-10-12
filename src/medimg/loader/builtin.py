"""Registration of built-in dataset adapters."""

from medimg.adapters.chestxdet10 import ChestXDet10Adapter, DATASET_METADATA
from medimg.registry.datasets import register_dataset, registered_dataset_names


def _create_chestxdet10(*, raw_dir):
    return ChestXDet10Adapter(raw_dir=raw_dir)


def register_builtin_datasets() -> None:
    if DATASET_METADATA.name not in registered_dataset_names():
        register_dataset(DATASET_METADATA, _create_chestxdet10)
