"""Dataset preparation and processed-data access."""

from medimg.loader.processed import DetectionDataset, detection_collate

__all__ = ["DetectionDataset", "detection_collate"]
