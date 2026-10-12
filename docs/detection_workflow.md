# Detection Workflow and Evaluation Protocol

This protocol is a pre-implementation recommendation for 2D chest-radiograph
bounding-box detection. It deliberately separates data facts from model
choices and forbids using a test set to make iterative decisions.

## 0. Prepare data before training

Training must read a versioned processed artifact, not parse source JSON/CSV,
decode DICOMs, or open compressed dataset archives in each epoch. A dataset
adapter performs that source-specific work once, validates annotations, and
materializes canonical images/targets plus a manifest under
`processed_data/<dataset>/<fingerprint>/`. This directory and its contents
are generated artifacts and must remain out of Git.

Preparation is deterministic and separately invokable from training. The
manifest records the dataset/schema version, source fingerprint inputs,
preprocessing format/settings, class mapping, and split counts. Training
validates the artifact and refuses missing or incompatible manifests; it does
not trigger an implicit preprocessing fallback. Stochastic augmentation,
sampling, and other epoch-varying transforms remain in the training data path
and operate on already prepared samples.

The first implementation materializes ChestX-Det10 images as native-size
grayscale `uint8` NPY arrays plus canonical JSONL targets. This avoids
repeated ZIP access, image decoding, and raw annotation parsing. Measure
throughput and storage before choosing a different representation for another
dataset. Keep source archives read-only and never delete them as part of cache
generation.

## 1. Data intake and preflight

Every dataset adapter should expose a read-only preflight that reports the
dataset/version, source files, checksums, sample counts, class support,
positive/empty-image counts, annotation counts, invalid boxes, missing image
references, image-read failures, dimensions, and split/group overlap.

Required checks before training:

1. Verify archive integrity and enumerate expected members without extracting
   to a versioned location.
2. Ensure every annotation record resolves to exactly one image and every
   image is accounted for by the expected manifest.
3. During preparation, decode images once and verify the annotation coordinate
   frame against the decoded image's true width and height.
4. Reject non-finite coordinates, non-positive box area, invalid category
   IDs, and coordinates outside image bounds; report the sample IDs rather
   than silently clipping or dropping records.
5. Render balanced overlays: each class, empty images, multiple boxes, small
   boxes, edge boxes, and random examples. Visually verify orientation,
   scaling, and class names.
6. Check image-, patient-, and study-level split overlap where identifiers
   exist. Save only aggregate diagnostics and non-identifying run metadata.
7. Check exact and likely duplicate images across splits; where feasible,
   inspect near-duplicates and shared patient/study identifiers. Do not claim
   independent test performance until the available grouping evidence has
   been reviewed.
8. Summarize image dimensions, box size/aspect ratio, boxes per image,
   per-class support, and empty-image prevalence by split. Flag material
   differences for review rather than silently rebalancing the official
   partitions.
9. Record source provenance, terms/citation status, annotation schema,
   preprocessing version, and a non-identifying aggregate report.

The known local ChestX-Det10 audit did not yet verify dimension consistency
or visual overlays. That is the first research gate.

## 2. Canonical sample and box contract

Adapters preserve native metadata, then convert to one documented in-memory
contract:

- Image: float tensor `[C, H, W]`, finite values and explicitly documented
  grayscale-to-model-channel policy.
- Boxes: float32 `[N, 4]`, absolute pixel coordinates in `xyxy` order
  (`x_min, y_min, x_max, y_max`) on the current image canvas.
- Labels: int64 `[N]`; contiguous dataset-specific foreground IDs. Background
  is implicit, not included in the annotation list. A model backend may apply
  a backend-specific background convention at its boundary.
- Empty/negative images: allowed and represented as correctly shaped empty
  box/label tensors. Do not fabricate a background box.
- Stable image/sample ID and, where allowed, a patient/study group key used
  for split checks. Keep identifiers out of public artifacts.
- Optional area/crowd fields are derived from transformed boxes and included
  only when required by the selected model/evaluator.

Every geometric transform must jointly transform image and boxes. Preserve
the native coordinates in the adapter and test round-trip/overlay behavior.
Torchvision's v2 transforms and `BoundingBoxes` types are one supported way
to keep these objects synchronized.

## 3. Dataset-specific boundaries

### ChestX-Det10

- Preserve the supplied training and official test partitions.
- Derive validation only from training. Prefer patient grouping if source
  identifiers are recoverable. If they are not, state and justify the
  limitation instead of assuming independent patients.
- Retain empty/no-box images; their treatment affects false positives per
  image.
- Keep the original ten-category ontology and the exact mapping from `syms`
  to model IDs versioned in configuration.
- Reproduce the authors' main protocol: IoU threshold 0.5 and recall at
  0.05, 0.1, and 0.2 instance-level false positives per image. The
  authors' `avgrecall` is the mean of those three values.
- Do not tune thresholds, image scale, classes, or model selection against the
  official test set.

### RSNA Pneumonia

- Treat this as a separate one-finding pneumonia task. It is not another
  split of ChestX-Det10.
- The CSV has multiple rows per positive image and blank box values for
  negatives; aggregate annotation rows per image before splitting.
- Split by `patientId`, not CSV row. Keep all boxes and the study's target
  together. Report internal validation separately from the unlabeled public
  competition test set.
- Decode DICOMs under a pinned, tested policy. `pixel_array`, transfer
  syntax/decode dependencies, modality rescale, photometric interpretation,
  VOI/windowing, inversion, and normalization all require explicit handling.
  Do not silently treat raw DICOM values as ordinary 8-bit RGB pixels.
- Review the current RSNA/Kaggle terms and required acknowledgments.

### SIIM-ACR and MAGIC-CT

- Keep SIIM out of the detector until the incomplete local archive is replaced
  with a verified, authorized source. Its RLE masks describe segmentation;
  any mask-to-box conversion would be a separate, explicitly defined task and
  would discard information.
- Keep MAGIC-CT out of this 2D workflow. It is 3D CT segmentation/report
  grounding, and its access agreement requires clarification before sharing
  restricted data.

## 4. Image processing and augmentation

Use deterministic validation/test preprocessing. Save the actual resize,
normalization, DICOM rendering, and channel policy in the experiment config
and checkpoint metadata.

For radiographs, do not enable a generic natural-image augmentation recipe by
default. Start with only justified geometric/photometric changes; make each
geometric transform update boxes; document horizontal flip's laterality
implications; avoid vertical flips and aggressive intensity/color changes
unless the scientific question supports them. Validate a sample grid before
training.

For DICOM, develop a separately testable renderer and a small set of fixture
tests covering photometric interpretation, image shape, dynamic range,
non-finite pixels, and decode failures. Cache rendered derivatives only in a
non-versioned data/cache location and record a content hash plus rendering
configuration.

## 5. Baselines and training

Keep the first baseline small and reproducible:

1. Use one supported two-stage detector as the initial reference, such as
   torchvision Faster R-CNN with a documented pretrained backbone; optionally
   add a one-stage RetinaNet comparator after the data/evaluation path passes.
2. Freeze the package versions, initialization source, input size, optimizer,
   schedule, batch size, epochs/stopping rule, augmentation, and seed in a
   checked-in experiment config.
3. Save the selected checkpoint by validation-only criteria. Never choose an
   epoch or threshold based on the official test score.
4. Run at least three independent seeds for a paper-quality stability
   estimate when compute permits. Report each seed and aggregate mean and
   dispersion; do not present the best seed as the expected result.
5. Track failed runs and resource constraints explicitly. Do not hide a
   missing optional backend or failed data read behind a successful-looking
   fallback.

YOLO/other detector families can be added through separate adapters after a
fixed baseline is reproducible. They should not expand the initial scope
without a research reason. Review dependency/model licensing and conversion
semantics before choosing a third-party training stack.

For a controlled comparison, define the primary outcome and baseline before
running experiments. Save the resolved config, code revision, dataset/cache
fingerprint, split manifest, class map, preprocessing settings, initialized
weight source, random seeds, runtime/library versions, evaluator version,
checkpoint-selection rule, and resource summary with each run. Change one
factor at a time in an ablation and retain unsuccessful runs in the experiment
record; do not report only the best result selected from many trials.

## 6. Metrics and statistical reporting

Never compare numbers unless the target, IoU, matching, averaging, and split
protocol match.

| Report | ChestX-Det10 pilot | RSNA follow-up | Purpose |
|---|---|---|---|
| Dataset-native primary | Recall at 0.05 / 0.1 / 0.2 FP per image, IoU 0.5; mean as authors' `avgrecall` | Use the official competition metric only when its evaluator and labeled split are available and reproduced; otherwise label the internal metric precisely | Comparability to the dataset/challenge protocol |
| Standard detection secondary | COCO-style AP averaged across IoU thresholds, plus AP50 and per-class AP | Same definitions may be reported as supplemental internal metrics | Cross-model comparability with explicit definitions |
| Diagnostic | Per-class support, recall, precision, FP/image, matched-IoU distribution, and error examples | Same, with negative-image false positives clearly included | Understand errors and class imbalance |
| Uncertainty | Per-seed values and confidence intervals; bootstrap by patient/study group when group IDs exist | Same | Avoid interpreting one split/seed as certainty |

Use a single pinned evaluator implementation and test it with hand-constructed
cases. Define duplicate detections, ignored/crowd labels, empty images,
confidence ties, and class-wise averaging. For box detection, do not report
image-classification AUROC/F1 as if they were localization metrics. For
segmentation, select segmentation metrics and a mask task definition instead.

The ChestX-Det10 authors' `avgrecall` is **not mAP**. Keep both only if their
definitions are stated and the official protocol is preserved.

## 7. Test-set discipline and result records

- Use train for fitting and validation for model/threshold decisions. Reserve
  each official test set for a small, predeclared final evaluation.
- Keep an experiment manifest with dataset/version and checksums, split
  definition, ontology mapping, code commit, config, seed, library/CUDA
  versions, checkpoint hash, evaluator version, and final metrics.
- Do not include raw sample IDs, images, DICOM metadata, or patient-level
  prediction outputs in public run artifacts.
- Store checkpoints, caches, logs containing sample-level outputs, and
  prediction visualizations outside Git by default.
- Separate exploratory validation runs from final confirmatory runs.

Maintain a compact failure-analysis record for important errors: error type
(miss, duplicate, localization, false positive, invalid/ambiguous annotation),
class and non-identifying context, likely cause, impact, proposed mitigation,
and the test that would verify a change. Aggregate examples and summaries
without exposing restricted images or patient identifiers.

Use staged acceptance gates: data/preflight passes; deterministic
preprocessing and target alignment pass; metric tests pass; a smoke train and
checkpoint reload pass; validation selection is reproducible; then conduct a
predeclared final test evaluation. Latency and memory are measured only when
relevant to the stated use case, and must include preprocessing if the
intended workflow includes it.

## Research references

- [PyTorch object-detection fine-tuning tutorial](https://docs.pytorch.org/tutorials/intermediate/torchvision_tutorial.html):
  dataset interface and target structure (`boxes`, labels, area, `iscrowd`).
- [Torchvision detection models](https://docs.pytorch.org/vision/stable/models/faster_rcnn.html):
  supported Faster R-CNN builders and model API.
- [Torchvision v2 transforms](https://docs.pytorch.org/vision/stable/transforms.html):
  transforms that jointly handle images and bounding boxes.
- [COCO evaluation overview](https://cocodataset.org/#detection-eval):
  standardized detection evaluation reference.
- [pydicom pixel-data guide](https://pydicom.github.io/pydicom/stable/tutorials/pixel_data/introduction.html):
  pixel decoding and DICOM image metadata considerations.
- [scikit-learn cross-validation guidance](https://scikit-learn.org/stable/modules/cross_validation.html):
  rationale for separating model selection from final test evaluation.
- Dataset-specific sources and terms are listed in
  [research findings](research_findings.md#primary-sources).
