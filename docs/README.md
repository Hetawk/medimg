# Medical Imaging Detection: Research Preparation

This folder captures the evidence review and design decisions for an
extensible medical-imaging package. The first prepare-first dataset pipeline
is implemented, but no local medical archives have been materialized, no model
has been trained, and no dataset has been uploaded.

## Documents

- [Project problem definition](problem_definition.md) — provisional research
  topic, dataset roles, candidate question, novelty gate, and study
  requirements.
- [Research findings and scope](research_findings.md) — local data readiness,
  candidate study directions, dataset limitations, and source links.
- [Detection workflow and evaluation protocol](detection_workflow.md) —
  annotation/data checks, splits, preprocessing, metrics, and experiment
  safeguards.
- [Modular architecture blueprint](architecture_blueprint.md) — registry- and
  config-driven support for multiple datasets, tasks, transforms, and models,
  plus CLI and notebook design.
- [Overall guide](overall-guide.md) — broader machine-learning task and
  engineering best-practice handbook.

## Current recommendation

Design the package to support multiple datasets, modalities, task types,
transform pipelines, and model families through explicit registries and
validated configs. Use ChestX-Det10 only as the first adapter and end-to-end
pilot—not as the framework's fixed scope. Keep RSNA as a separate pneumonia
task with its own data protocol. Do not combine datasets into one label space
or describe the pilot as cross-dataset generalization without a justified
shared ontology and study design. SIIM-ACR remains blocked until a complete,
authorized image/mask source is verified.

The first implementation gate is not model training: verify image dimensions,
annotation-to-image correspondence, patient/study grouping where available,
and representative box overlays. Materialize validated data separately from
training and consume the resulting versioned cache during model runs. Only
proceed to a fixed baseline after these checks pass. The paper question is
still provisional; follow the review and decision gates in
[the project problem definition](problem_definition.md) before making a
novelty claim or implementing a training study.

## Current implementation boundary

- The first raw adapter, preparation cache, processed-data reader, and CLI are
  implemented for ChestX-Det10.
- Additional dataset adapters, task/transform/model registries, training,
  evaluation, and the notebook remain follow-up work.
- Treating classification, box detection, and segmentation metrics as
  interchangeable.
- Adding a large model zoo before a baseline protocol is justified.
- Putting images, derived patient-level data, credentials, or checkpoints in
  Git.

These are design recommendations, not clinical-use claims. Any study requires
dataset-specific citation, terms review, and an appropriately described
validation protocol.
