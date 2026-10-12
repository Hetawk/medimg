# Research Findings and Study Scope

## Executive assessment

The local resources are a useful starting point for a **2D chest X-ray object
detection engineering pilot**, but they do not yet support one coherent,
multi-dataset paper with a shared target. ChestX-Det10 annotates ten thoracic
abnormality categories; RSNA annotates pneumonia; SIIM-ACR is a pneumothorax
**segmentation** challenge and its local archive is unreadable. These are
different label spaces and, for SIIM, a different prediction target.

The defensible sequence is:

1. Validate ChestX-Det10 images, boxes, splits, and visual overlays.
2. Reproduce a documented detector baseline and the dataset's own evaluation
   protocol without tuning on its official test set.
3. Add RSNA only as a separate pneumonia-detection experiment with a separate
   adapter and protocol.
4. Decide whether there is a research question beyond a baseline comparison.
   Only consider cross-dataset claims after a class-by-class ontology,
   provenance, and split audit.

An ordinary model leaderboard on one or two public datasets is useful
engineering, but is not by itself a strong novelty claim. A paper needs a
specific hypothesis, a defensible comparator, uncertainty/error analysis, and
an evaluation design aligned with that hypothesis.

## Local evidence and readiness

The following counts come from the local annotation/archive review documented
in [dataset_assessment.md](../dataset_assessment.md). They are structural
checks, not a clinical-quality review.

| Dataset | Task and local evidence | Assessment |
|---|---|---|
| ChestX-Det10 | 3,001 train and 542 test records; 6,863 and 1,476 boxes; all ten labels occur in both splits. The train/test JSON arrays agree in length per record; coordinates are finite, positive-area `xyxy` boxes with non-negative origins. Image archives pass ZIP integrity checks. | Best first pilot. Still verify decoded image dimensions, image-name coverage, patient/study separation if identifiers are available, and visual overlays. Train validation must come only from the supplied training split. |
| RSNA Pneumonia Detection Challenge | 26,684 labeled training DICOMs and 3,000 unlabeled test DICOMs. The training CSV has 30,227 rows: 9,555 positive box rows across 6,012 positive images and 20,672 negative rows. Positive box fields passed basic numeric checks. | Technically usable as a distinct pneumonia task. Review current access/attribution terms; use `patientId` to group internal train/validation partitions. The public test set has no labels in the local archive. |
| SIIM-ACR Pneumothorax | The local 328 MiB file is named `.zip`, but archive listing and integrity checks fail because it has no usable central directory. | Blocked. Do not treat the archive as a complete dataset or attempt to train from it. Revisit only after obtaining and verifying a complete, authorized image/mask source. Its RLE masks define a segmentation task, not a box-detection task. |
| VinDr-CXR (not locally staged) | The primary dataset description reports 18,000 PA radiographs, with 22 localized finding labels and six global diagnosis labels; it describes 15,000 training and 3,000 test images. The images are DICOM and the dataset has access/usage requirements. | A possible future external dataset, not an automatic drop-in. Check current PhysioNet terms, annotation schema, class definitions, reader protocol, and download/storage budget before access. The six global labels are not box labels. |
| MAGIC-CT (source note only) | The local discovery note describes volumetric CT segmentation, lesion masks, and reports, with a restricted-data-use agreement despite a record-level CC0 label. | Separate 3D segmentation/multimodal project. Do not mix into this 2D chest-X-ray detector; resolve the apparent license/DUA relationship with the dataset owner before collaborative access. |

### Important correction about VinDr-CXR

Do not describe VinDr-CXR as having 28 localized findings. Its primary
description distinguishes **22 local labels with bounding boxes** from **six
global labels**. A global diagnosis must not be converted into a box target
without a separate, defensible localization annotation.

### Terms and handling

- Public download availability is not a blanket license to redistribute.
- The RSNA organizer's page permits research/education and other use subject
  to its stated attribution requirements. Check the current dataset rules and
  acknowledgments before publishing or sharing data.
- ChestX-Det10's repository gives citation and download instructions, but no
  explicit license grant was found in the inspected README. Review both the
  dataset and source NIH data terms before redistribution.
- VinDr-CXR requires following the current PhysioNet access/usage terms and
  citing both the dataset and repository.
- Keep raw datasets, per-image outputs, patient/study identifiers, access
  tokens, and checkpoints out of Git. Preserve the existing
  [`.gitignore`](../.gitignore) protections for `.env` and `datasets/`.

## Candidate research directions

### A. Reproducible ChestX-Det10 localization baseline — recommended pilot

Implement the official parser/preflight checks, inspect box overlays, and
compare one well-defined detector baseline with the dataset's reference metric.
The authors specify recall (sensitivity) at 0.05, 0.1, and 0.2 instance-level
false positives per image, using IoU 0.5; their `avgrecall` averages those
three recall values. Report this protocol rather than silently replacing it
with mAP. COCO-style AP can be reported as a secondary standardized metric.

**Contribution potential:** low if it is only a standard model run. It is a
necessary validation pilot and a useful reproducibility/engineering result,
not a novelty claim by itself.

### B. RSNA pneumonia localization — separate follow-up task

Build a second adapter only after the first data path works. Keep RSNA's
pneumonia label, DICOM rendering, negative studies, and official competition
evaluation distinct. Split the labeled cohort by `patientId`; never split
individual CSV box rows. Do not claim an official held-out test result when
using the unlabeled public competition test archive.

**Contribution potential:** useful for a pneumonia-specific study, but simply
adding a second dataset with unrelated labels does not establish
cross-dataset generalization.

### C. Cross-dataset localization under domain/annotation shift — possible
later paper question

This requires (1) a named shared target with clinical/annotation
justification, (2) image-level and patient-level separation, (3) consistent
box and negative-label semantics, and (4) an external test source not used to
choose models or thresholds. The present ChestX-Det10 and RSNA label sets do
not provide a straightforward shared multi-class ontology. VinDr-CXR may be
evaluated for candidate label overlap, but overlap must be checked from the
annotation definitions, not inferred from similar words.

**Do not claim:** a universal medical detector, general clinical
generalization, or cross-hospital robustness from a standard run on these
datasets alone.

### D. SIIM-ACR masks or MAGIC-CT — out of scope for this project phase

SIIM-ACR's mask/RLE target is segmentation. MAGIC-CT is 3D CT with masks and
report grounding. Either could be a valuable future project, but each calls
for a distinct data pipeline, model outputs, and evaluation plan. First
verify the data source and terms.

## Study questions to decide after the pilot

Use the pilot evidence to choose one focused paper hypothesis, for example:

- How much do detector results change when evaluation follows the dataset's
  original low-FP-per-image protocol instead of a generic AP-only report?
- Which classes and box-size strata account for localization errors, and how
  stable are results across independent training seeds?
- Does a prespecified, ontology-valid external dataset show a measurable
  domain shift for one shared finding?

These are candidate questions, not novelty claims. Select one only after
literature review, data validation, and a clear comparator/analysis plan.

## Primary sources

1. Liu, Lian, and Yu, [*ChestX-Det10: Chest X-ray Dataset on Detection of
   Thoracic Abnormalities*](https://arxiv.org/abs/2006.10550); dataset schema,
   evaluation protocol, and citation are also in the
   [authors' repository](https://github.com/Deepwise-AILab/ChestX-Det10-Dataset).
2. RSNA, [2018 Pneumonia Detection Challenge information and terms /
   attribution](https://www.rsna.org/artificial-intelligence/ai-image-challenge/rsna-pneumonia-detection-challenge-2018);
   [Kaggle dataset page](https://www.kaggle.com/competitions/rsna-pneumonia-detection-challenge/data)
   and [competition rules](https://www.kaggle.com/competitions/rsna-pneumonia-detection-challenge/rules).
3. Nguyen et al., [VinDr-CXR on PhysioNet](https://physionet.org/content/vindr-cxr/1.0.0/),
   including dataset description, split, DICOM format, and citation.
4. SIIM-ACR, [Pneumothorax Segmentation competition data
   page](https://www.kaggle.com/competitions/siim-acr-pneumothorax-segmentation/data).
5. MAGIC-CT, [Zenodo record 18389015](https://zenodo.org/records/18389015).

## Open questions before research claims

- Can ChestX-Det10 image dimensions and all boxes be confirmed against the
  actual decoded images? Are the published split files patient-disjoint?
- Which training-only validation split can be created without leaking
  patients/studies? If source identifiers are unavailable, what limitation
  must be reported?
- What detector and training recipe provide the simplest reproducible
  comparator under available hardware?
- Is the goal a dataset-specific pilot, a method contribution, or a
  cross-dataset generalization study? The answer determines which datasets,
  metrics, and comparisons are appropriate.
