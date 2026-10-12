"""Shared contracts for dataset preparation and processed samples."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Protocol

import numpy as np


@dataclass(frozen=True)
class DatasetMetadata:
    name: str
    task: str
    class_names: tuple[str, ...]
    description: str


@dataclass(frozen=True)
class PreparationResult:
    dataset_dir: Path
    reused: bool
    image_counts: dict[str, int]


class DatasetAdapter(Protocol):
    """Raw-source adapter that materializes one canonical processed dataset."""

    metadata: DatasetMetadata

    def prepare(
        self,
        out_dir: Path,
        *,
        force: bool = False,
        progress: Callable[[str, int, int], None] | None = None,
    ) -> PreparationResult:
        """Create or reuse the prepared artifact for the raw dataset."""


class SampleTransform(Protocol):
    def __call__(self, image: np.ndarray, target: dict[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
        """Transform an image and all spatial targets together."""


AdapterFactory = Callable[..., DatasetAdapter]
