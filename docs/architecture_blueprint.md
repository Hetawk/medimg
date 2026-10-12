# Modular Medical-Imaging Architecture Blueprint

This is a proposed extensible framework, not an implementation. The aim is
to make new datasets, modalities, task types, transforms, and model families
pluggable through small explicit interfaces and configuration—not to build a
framework hard-wired to ChestX-Det10. The first experiment can still be
ChestX-Det10; that is a validation milestone, not an architectural boundary.

## Design principles

1. **Dataset adapters describe data; they do not own training.** An adapter
   parses one source and declares its modality, task capabilities, labels,
   split metadata, decoder, and native evaluation rules.
2. **Tasks define output contracts.** Detection boxes, segmentation masks,
   image classification labels, and multi-label findings are not interchangeable.
   They may share infrastructure, but they keep distinct target and metric
   contracts.
3. **Transforms are composable and task-aware.** Each dataset selects a
   transform pipeline in config. Geometric transforms declare which target
   structures they transform; the framework rejects incompatible pipelines.
4. **Models declare capabilities and requirements.** The model registry
   resolves a model by name only when requested; each model declares supported
   task(s), input modalities, target format, and optional dependencies.
5. **Configuration is explicit and reproducible.** A run is resolved from a
   checked-in YAML configuration plus CLI overrides. The resolved config is
   validated and saved with the run.
6. **Keep shared code genuinely shared.** Do not force every dataset into
   common label semantics, image normalization, or evaluation. Keep
   source-specific rules at adapter/protocol boundaries.

## Learn from MedDef, do not copy its assumptions

Useful MedDef patterns include a central
[model orchestrator](../../../latex/meddef/model/model_loader.py),
[dataset loader](../../../latex/meddef/loader/dataset_loader.py), shared
[argument parser](../../../latex/meddef/argument_parser.py), and separate
training/evaluation utilities:

- One stable entry point routes requested names and settings to implementation
  families.
- Dataset, model, training, metrics, visualization, and run management have
  dedicated purposes.
- A command-line interface controls experiments consistently.

The new project must improve on the specifics:

- MedDef's current loader uses classification-oriented `ImageFolder`; this
  cannot express variable-length boxes, masks, empty images, study groups, or
  dataset-native annotation semantics.
- Do not import every model backend at startup or turn missing optional
  dependencies into a warning followed by a misleading partial run. Resolve
  only the selected implementation and fail clearly when it is unavailable.
- Avoid one ever-growing parser full of unrelated flags. Use subcommands,
  validated dataset/model registries, configuration files, and scoped
  overrides.

## Extensible package layout

`medimg` is a placeholder package name. This layout supports future datasets
and tasks without requiring all of them to be implemented in the first pass.

```text
medical/
├── configs/
│   ├── datasets/
│   │   ├── chestxdet10.yaml
│   │   ├── rsna_pneumonia.yaml
│   │   └── vindr_cxr.yaml
│   ├── transforms/
│   │   ├── cxr_detection_train.yaml
│   │   └── cxr_eval.yaml
│   └── experiments/
│       └── chestxdet10_fasterrcnn.yaml
├── docs/
├── notebooks/
│   └── workbench.ipynb
├── processed_data/                 # generated, ignored cache; never committed
├── src/medimg/
│   ├── cli.py
│   ├── config/
│   │   ├── loader.py
│   │   └── validation.py
│   ├── registry/
│   │   ├── datasets.py
│   │   ├── models.py
│   │   ├── transforms.py
│   │   ├── tasks.py
│   │   └── metrics.py
│   ├── loader/
│   │   ├── contracts.py
│   │   ├── factory.py
│   │   ├── processed.py
│   │   ├── preflight.py
│   │   ├── splitters.py
│   │   ├── decoders/
│   │   │   ├── raster.py
│   │   │   └── dicom.py
│   ├── adapters/
│   │   ├── chestxdet10.py
│   │   ├── rsna_pneumonia.py
│   │   └── vindr_cxr.py
│   ├── tasks/
│   │   ├── detection/
│   │   │   ├── contracts.py
│   │   │   └── evaluator.py
│   │   ├── segmentation/
│   │   │   ├── contracts.py
│   │   │   └── evaluator.py
│   │   └── classification/
│   │       ├── contracts.py
│   │       └── evaluator.py
│   ├── transforms/
│   │   ├── compose.py
│   │   ├── geometric.py
│   │   ├── intensity.py
│   │   └── registry.py
│   ├── models/
│   │   ├── factory.py
│   │   ├── detection/
│   │   │   ├── torchvision_fasterrcnn.py
│   │   │   └── torchvision_retinanet.py
│   │   ├── segmentation/
│   │   └── classification/
│   ├── engine/
│   │   ├── trainer.py
│   │   ├── evaluator.py
│   │   └── checkpoint.py
│   ├── metrics/
│   │   ├── detection/
│   │   │   ├── coco.py
│   │   │   └── chestxdet10.py
│   │   └── segmentation/
│   ├── visualization/
│   └── runs/
│       ├── manifest.py
│       └── paths.py
├── tests/
│   ├── fixtures/
│   ├── contracts/
│   ├── adapters/
│   ├── transforms/
│   ├── models/
│   └── metrics/
├── .gitignore
└── pyproject.toml
```

`loader/` contains the preparation contracts and processed-data reader. Raw
dataset-specific parsers live in the sibling `adapters/` package. Raw
datasets stay under the root `/datasets/` directory and are excluded from
Git; package code remains under `src/medimg/`.

Do not create empty scaffolding for every future modality. Add a task family
only when a concrete dataset and experiment need it. The registry contracts
are designed to permit growth without building a large model zoo or an
overgeneralized abstraction up front.

## Prepare-first data lifecycle

The framework has two explicit data phases:

```text
raw source files (read-only)
        │
        ▼
dataset adapter + preparation pipeline
  validate → decode → canonicalize → materialize
        │
        ▼
versioned processed artifact
  images + canonical annotations + manifest
        │
        ▼
processed dataset reader
        │
        ▼
training-time task transforms → model
```

Training and evaluation must consume the processed artifact, not reopen raw
archives, parse source annotation formats, or decode DICOM at each epoch.
Dataset adapters are responsible for the one-time expensive/source-specific
work: archive access, decoding, source-label validation/mapping, canonical
annotation serialization, and cache provenance. Training-time transforms are
still applied when they are stochastic or need to vary per epoch; deterministic
source decoding and canonicalization belong in preparation.

Processed outputs live under ignored `processed_data/<dataset>/<fingerprint>/`.
Each artifact contains a schema-versioned manifest, per-split canonical
annotation JSONL, and predecoded NPY arrays. The cache key includes annotation
content hashes, source archive size/mtime metadata, schema, and preprocessing
settings. Reuse is allowed only when a matching manifest exists; an incomplete
or incompatible cache is an explicit error. Never overwrite raw data.

Materialized image representation is a dataset/preprocessing decision:
ChestX-Det10's initial materializer writes native-resolution grayscale
`uint8` arrays and leaves boxes in the same absolute `xyxy` pixel coordinates.
It avoids repeated ZIP access, PNG decoding, and JSON parsing while keeping
variable image dimensions intact. Other adapters may choose another format
after measuring training throughput, disk cost, and fidelity; the
processed-data contract and manifest must identify that choice. Do not
silently bake train augmentations into the cache.

Preparation is its own CLI operation, separate from model training:

```text
medimg prepare -d chestxdet10 --raw datasets/chestxdet10 --out processed_data
medimg inspect --data processed_data/chestxdet10/<fingerprint> -s train
medimg train --config configs/experiments/chestxdet10_fasterrcnn.yaml
```

The trainer must require the prepared artifact path and validate its manifest
before creating the model. It must not implicitly fall back to raw files or
launch processing inside the training loop. This makes preprocessing costs
visible and lets subsequent runs reuse the same validated artifact.

## Plugin contracts and registries

Use explicit registration (initially Python registration functions or
decorators) with stable public names. A plugin descriptor should carry
metadata as well as a builder, so the CLI can list valid choices and validate
compatibility before loading data or allocating a GPU.

### Dataset descriptor

Each dataset descriptor declares:

- name, version/source citation, modality, and supported task types;
- adapter factory and required/optional config keys;
- image/volume decoder and channel/intensity policy;
- native annotation schema and conversion to the task contract;
- available splits, group-key semantics, class ontology, and native metric
  protocol;
- data-use notes and expected input paths.

A raw adapter under `adapters/` reads one source format. The `loader/` package
owns preparation, source decoders, split helpers, canonical data contracts,
and the training-facing reader for processed outputs. These packages do not
select a model, augmentation recipe, or optimizer.

### Model descriptor

Each model descriptor declares:

- supported task types and input modalities;
- accepted target contract and any explicit conversion;
- required/optional config fields and minimum dependency/backend;
- builder and inference-output contract.

Resolve and import only the chosen model. Unknown names, incompatible task
types, invalid options, and missing dependencies are hard, actionable errors.
Never fall back silently to another architecture.

### Transform descriptor

Each transform declares:

- supported data types (image, boxes, masks, volumes, labels);
- whether it is deterministic and whether it is train-only;
- required parameters and value constraints;
- how it changes spatial metadata and target annotations.

Compose dataset-specific pipelines from named transforms. At config-validation
time, reject a geometric transform that would modify pixels but not boxes or
masks. Keep train transforms separate from deterministic validation/test
transforms. Decoder/rendering operations are explicit preprocessing stages,
not hidden global defaults.

### Task and metric descriptors

Task contracts describe targets and prediction outputs. A detection protocol
can expose both dataset-native metrics and a standardized metric; a
segmentation protocol exposes mask metrics. Do not make a dataset descriptor
pretend that image labels are localization targets. Dataset-native metrics
are selected by the dataset/task configuration and remain separately named.

## Configuration and command-line design

Use a small argparse-based CLI with subcommands. Keep conventional module
names short (`data`, `models`, `tasks`, `transforms`, `metrics`, `engine`,
`adapters`) and reserve longer names for domain concepts where they improve
clarity. CLI options should have compact, memorable forms: `-d/--dataset`,
`--raw`, `--out`, `--data`, `-s/--split`, `-n/--samples`, and `-f/--force`.
Do not add aliases for every spelling. The CLI discovers options
from registries and reads a dataset/experiment YAML. CLI flags override
configuration values; the final merged config is validated, printed or
summarized before a costly run, and saved as `resolved_config.yaml`.

Example commands:

```text
python -m medimg.cli datasets list
python -m medimg.cli datasets inspect chestxdet10
python -m medimg.cli models list --task detection
python -m medimg.cli transforms list --task detection
python -m medimg.cli preflight --config configs/datasets/chestxdet10.yaml
python -m medimg.cli visualize --config configs/datasets/chestxdet10.yaml --count 24
python -m medimg.cli train --config configs/experiments/chestxdet10_fasterrcnn.yaml --seed 17
python -m medimg.cli evaluate --run-id <run-id> --split test
```

Proposed responsibilities:

- `datasets list/inspect`: registry choices, capabilities, configuration
  schema, declared splits, and data path status.
- `models list`: only models compatible with the requested task.
- `preflight`: validate paths, data integrity, annotations, splits, and
  ontology before training.
- `visualize`: use the selected adapter and transform configuration to render
  sample/box or mask overlays.
- `train/evaluate`: instantiate the resolved config through factories and
  shared task contracts.

Keep `argparse` responsible for command structure and simple overrides, not
for duplicating every model/dataset-specific field. Validate the YAML against
the selected plugin's schema. Support explicit `--set section.key=value`
overrides only if type conversion and error messages are reliable; ordinary
typed flags such as `--seed`, `--device`, `--epochs`, and `--output-dir` are
preferable for common controls.

Example config:

```yaml
dataset:
  name: chestxdet10
  root: ${MEDIMG_DATA_ROOT}/chestxdet10
  split_policy:
    validation_fraction: 0.15
    group_by: patient_id
task:
  name: detection
  metric_protocol: chestxdet10
transforms:
  train: cxr_detection_train
  evaluation: cxr_eval
model:
  name: torchvision_fasterrcnn
  pretrained: true
training:
  seed: 17
  epochs: 40
  batch_size: 4
```

`${MEDIMG_DATA_ROOT}` is illustrative: resolve environment variables through
a documented config mechanism, never by reading secrets into logs. Dataset
configs must not store credentials.

## Data and task contracts

The common dataset interface should be small: expose dataset metadata,
split-specific sample access, and preflight. Do not impose a single physical
representation on all modalities. A task adapter converts the dataset-native
sample into the selected task contract.

For 2D box detection, the initial task contract is:

- image tensor `[C,H,W]` after explicit decoder/rendering policy;
- absolute `xyxy` float boxes on the current canvas and integer foreground
  labels;
- valid empty targets for negative images;
- sample identity/group metadata kept internal to split checks and excluded
  from public per-image artifacts.

Segmentation, classification, and 3D tasks must define their own target
contracts. Common run management, configuration, reproducibility, and
visualization helpers may be shared where semantics genuinely match.

## Training, evaluation, and output responsibilities

- **Trainer:** optimization, scheduler, mixed precision, seeded execution,
  validation cadence, and checkpoint selection.
- **Evaluator:** inference and task-agnostic collection of predictions and
  targets under an explicit split.
- **Metric protocol:** matching rules, thresholds, aggregation, empty-target
  behavior, and named outputs.
- **Dataset evaluator adapter:** bridges the generic task outputs to
  dataset-native scoring rules without redefining the model.
- **Run manager:** config, code revision, seed, data manifest hashes, runtime
  versions, checkpoints, logs, and metric-definition metadata.
- **Visualization:** dataset-aware decoding and target overlays; output
  location and retention follow data terms.

Artifacts and caches default outside the repository. Public outputs must not
contain restricted images, DICOM metadata, patient identifiers, or
sample-level predictions unless terms explicitly permit publication.

Each run should also retain a compact failure/ablation record: what changed,
the hypothesis, validation-only selection criterion, outcome (including
failed runs), and any observed data/model failure mode. Do not let a run
manager become an experiment tracker full of duplicate metadata; keep one
resolved config and link each result to its prepared-data fingerprint and
code revision.

## Notebook as a client of the package

Build the notebook after stable package APIs exist. It should call the same
registries, preflight, visualization, training, and evaluation APIs as the
CLI. It can provide interactive dataset/model/transform selection, overlay
inspection, a small smoke run, and result plots. It must not duplicate parser,
transform, trainer, metric, or model-building code. Strip output cells that
could expose restricted data or make notebook diffs enormous.

## Test-first extension gates

1. **Data checks:** schema/range checks, corrupt or missing inputs, duplicate
   records, image-to-annotation coverage, split/group leakage, and
   class/box-distribution summaries.
2. **Core contracts:** synthetic fixtures for variable-size detection,
   empty targets, segmentation masks, classification labels, and modality
   metadata.
3. **Registry and CLI:** registration, listing, invalid name, incompatible
   task/model, bad config field, and missing optional dependency produce clear
   behavior before data/GPU initialization.
4. **Transform compatibility:** image/box/mask alignment after geometric
   transforms; evaluation transform determinism; invalid pipeline rejection.
5. **First dataset adapter:** ChestX-Det10 parse and preflight using fixtures,
   then local read-only materialization and processed-reader checks.
6. **Metric protocols:** synthetic predictions prove matching, duplicate
   false positives, empty images, and dataset-specific aggregation.
7. **First model:** minimal forward/backward, checkpoint reload, and
   validation-only selection.
8. **Additional datasets:** add RSNA/VinDr through adapter/config/tests while
   reusing contracts and keeping DICOM rendering and patient grouping specific.
9. **Additional tasks/models:** add only after a concrete experiment requires
   them; prove plugin compatibility and maintain all existing adapters.
10. **Notebook:** integrate after public APIs stabilize; test against synthetic
   or authorized sample fixtures.

These layers implement the handbook's data, unit, integration, and model
acceptance testing recommendations. Serving and production-monitoring tests
are deferred because this repository currently targets offline research, not
a deployed clinical system.

## Dependency and maintenance principles

- Keep the core environment small; make model backends and modality decoders
  optional extras selected by feature.
- Pin and record tested framework/runtime versions and pretrained-weight
  source/license.
- Import optional dependencies lazily and make failures explicit.
- Keep configs typed, validated, and versioned. Avoid hidden
  dataset-dependent defaults.
- Preserve `.env` and dataset exclusions in
  [`.gitignore`](../.gitignore); keep raw data, caches, and checkpoints out of
  Git by default.
