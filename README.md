# Medical Imaging Research

Modular research code for medical-imaging datasets and models. Raw archives
remain untouched; the training-facing data API reads versioned, prepared
artifacts from `processed_data/`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Install the optional PyTorch dependencies for model training:

```bash
python -m pip install -e ".[train,dev]"
```

## Prepare ChestX-Det10

The raw dataset root should contain `annotations/train.json`,
`annotations/test.json`, `train_data.zip`, and `test_data.zip`.

```bash
medimg datasets list
medimg prepare \
  -d chestxdet10 \
  --raw datasets/chestxdet10 \
  --out processed_data
```

The processor reads the source archives without extracting or modifying them,
validates annotation/image correspondence and box bounds, and writes
`uint8` grayscale `.npy` images with canonical `xyxy` boxes and zero-based
foreground labels. The generated location is fingerprinted from source
annotation hashes, archive file metadata, schema, and preprocessing settings.
Rerunning preparation reuses a matching cache. Pass `--force` to rebuild that
cache.

Inspect and load only the processed artifacts:

```bash
medimg inspect \
  --data processed_data/chestxdet10/<fingerprint> \
  -s train
```

```python
from medimg.loader import DetectionDataset, detection_collate

train_set = DetectionDataset(
    "processed_data/chestxdet10/<fingerprint>",
    split="train",
)
sample = train_set[0]
```

`DetectionDataset` returns a grayscale `uint8` NumPy image, canonical
box/label targets, and sample metadata. `detection_collate` keeps variable-size
images and targets as lists for a PyTorch `DataLoader`. The trainer/model
integration will convert these processed arrays into model tensors; it must
not reopen raw sources during training.

## Processed-data boundary

```text
raw archive + native annotations
               │
               ▼
dataset adapter: validate, decode, canonicalize, materialize
               │
               ▼
processed_data/<dataset>/<fingerprint>/
  dataset_manifest.json
  train/annotations.jsonl + images/*.npy
  test/annotations.jsonl  + images/*.npy
               │
               ▼
processed dataset reader → task transforms → model/trainer
```

The implemented code currently covers dataset registration, ChestX-Det10
materialization, processed-data reading, and preparation/inspection CLI
commands. Model registries, training loops, task transform implementations,
and additional raw dataset adapters are subsequent implementation steps.

`datasets/`, `processed_data/`, `outputs/`, and `.cache/` are ignored by Git.
Commit code, configs, dataset instructions, and test fixtures—not raw or
processed medical images, caches, checkpoints, or sample-level predictions.
See [the architecture blueprint](docs/architecture_blueprint.md) for extension
contracts and [the research findings](docs/research_findings.md) for dataset
scope and terms.
