"""Dataset adapter registry with explicit names and lazy factories."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from medimg.loader.contracts import AdapterFactory, DatasetMetadata


@dataclass(frozen=True)
class DatasetRegistration:
    metadata: DatasetMetadata
    factory: AdapterFactory


_DATASETS: dict[str, DatasetRegistration] = {}


def register_dataset(
    metadata: DatasetMetadata, factory: AdapterFactory
) -> None:
    if not metadata.name or metadata.name in _DATASETS:
        raise ValueError(f"Dataset name is empty or already registered: {metadata.name!r}")
    _DATASETS[metadata.name] = DatasetRegistration(metadata, factory)


def get_dataset(name: str) -> DatasetRegistration:
    try:
        return _DATASETS[name]
    except KeyError as exc:
        available = ", ".join(sorted(_DATASETS)) or "(none)"
        raise ValueError(f"Unknown dataset {name!r}. Available datasets: {available}") from exc


def list_datasets() -> tuple[DatasetMetadata, ...]:
    return tuple(_DATASETS[name].metadata for name in sorted(_DATASETS))


def create_dataset(name: str, **kwargs: Any):
    return get_dataset(name).factory(**kwargs)


def registered_dataset_names() -> tuple[str, ...]:
    return tuple(sorted(_DATASETS))
