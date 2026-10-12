# Medical detection dataset assessment

Reviewed 2026-10-08; local inventory and annotation status verified
2026-10-08. This note evaluates the Zenodo record in [`source.md`](source.md),
nearby annotation-ready datasets, access terms, and whether they fit a first
detection project.

## Recommendation in brief

- **For a fast, compact 2D chest-X-ray detection baseline:** start with
  **ChestX-Det10**. Its 3,001 training and 542 test records contain 6,863 and
  1,476 boxes, respectively, across 10 findings. The local JSON structure and
  box geometry passed basic integrity checks; the published image archives
  total about 1.43 GB.
- **For a paper using multiple datasets:** ChestX-Det10 and RSNA are the two
  currently usable candidates, but their targets and protocols differ. Keep
  results separate; two unrelated benchmark tables alone are not a strong
  research contribution. The local SIIM-ACR archive is structurally
  incomplete, and the official Kaggle instructions say the training images
  came from a Cloud Healthcare API that is no longer available. Do not count
  SIIM as a usable dataset unless a complete, authorized source is verified.
- **Do not combine all candidate datasets into one training pool by default.**
  They differ in findings, annotation policy, and label format. Separate
  dataset-specific results are easier to interpret; only compare a shared
  finding when its definitions and evaluation protocol are genuinely
  compatible.
- **VinDr-CXR is a strong but larger option, not the compact first choice.**
  It provides 18,000 images and boxes for 22 local findings, but the available
  Zenodo archives total about 48.0 GB.
- **For 3D CT lesion segmentation:** ULS23 is a well-structured challenge
  resource with masks/volumes of interest, but it is a large, multi-source
  collection and carries a CC BY-NC-SA 4.0 license. It is not a drop-in 2D
  YOLO dataset.
- **Do not treat MAGIC-CT as unrestricted shared data yet.** Its Zenodo
  metadata says open/CC BY 4.0, its description says CC0-1.0, and the record
  text also contains a data-use agreement that requires an application and
  says not to share access. These terms conflict. Ask the contact author to
  resolve them in writing before downloading for a team project or
  redistributing anything.
- **Treat this as a standalone project.** Choose a dataset based on the new
  project's target domain and annotation type; do not assume any dataset,
  code, or results from another project apply here.

## Candidate comparison

| Dataset | What is already annotated | Files/access observed | Fit and caveats |
|---|---|---|---|
| [VinDr-CXR on Zenodo](https://zenodo.org/records/12721389) / [official PhysioNet record](https://physionet.org/content/vindr-cxr/1.0.0/) | 18,000 adult PA chest X-rays. 22 local findings have bounding boxes; 6 diagnoses are image-level labels. Training images have annotations from 3 readers; test labels are consensus from 5 readers. | Zenodo lists `vindr_train.zip` (40,450,822,525 bytes) and `vindr_test.zip` (7,581,545,663 bytes), about 48.0 GB total. Zenodo metadata says CC BY 4.0. Images/labels are DICOM + CSV on the official record. | **Strong larger-scale 2D detection option, but not a compact first pick.** The user note says 28 localized findings; correction: 22 are localized, while the other 6 are global labels. Prefer official PhysioNet documentation/terms; treat the Zenodo copy as a mirror and verify provenance/attribution before relying on its separate CC BY metadata. Keep the official train/test split and resolve how to handle multiple reader boxes. |
| [MAGIC-CT v2](https://zenodo.org/records/18389015) | Record description reports 562 CT patients with 3D organ/lesion masks; 492 also have radiologist-authored reports, totalling 4,937 organ descriptions, across 8 pathologies and 4 organs. | The current Zenodo API lists 21 files totalling about 39.14 GB by file sizes. The page reports 2.5 TB data volume; that is a different figure and likely reflects expanded data, but the discrepancy has not been independently reconciled. Zenodo metadata says open/CC BY 4.0; the description itself says CC0-1.0. | **Potentially valuable for 3D segmentation and report grounding, not ready-made 2D detection.** Its DUA says access is by application, requires human-subject/HIPAA training, and forbids sharing access. The DUA, description license, and Zenodo license metadata conflict. Do not assume the public badge overrides the DUA; obtain written clarification before using it in collaborative annotation or sharing. |
| [ULS23 Part 2](https://zenodo.org/records/10050960), [Part 3](https://zenodo.org/records/10054306), [official challenge](https://uls23.grand-challenge.org/) | 3D CT lesion volumes of interest/segmentations. Part 2 describes 333 kidney, 2,246 lung, and 888 liver lesions; Part 3 includes lesions from several public challenge datasets. The challenge combines new annotated data with existing sources. | Split across multiple large, multipart ZIP archives; individual parts are tens of GB. License stated as CC BY-NC-SA 4.0. | **Good second choice if the research question is universal 3D lesion segmentation.** More setup than VinDr and not direct 2D bounding boxes. Check upstream dataset terms as well as the ULS23 license; the collection includes third-party source datasets. |
| [IMA++ skin-lesion segmentation](https://zenodo.org/records/14201693) | 17,684 masks across 14,967 dermoscopic images; 2,394 images have 2–5 annotations. The files include 22,472 masks including STAPLE/majority-vote consensus, metadata, inter-annotator metrics, and standard splits. | `segs.zip` is about 162 MB. The actual images must also be obtained from the linked [ISIC collection](https://api.isic-archive.com/collections/482/). Zenodo metadata lists CC BY-NC-ND 4.0. | **Useful for 2D segmentation and annotation-variability experiments, not box detection.** It is relatively small to inspect, but the images are separate and the non-commercial/no-derivatives license is restrictive. Do not convert masks to boxes or publish derivative annotations without confirming permission. |
| [CRADI](https://zenodo.org/records/5493595) | 25 report-derived image-level labels; no lesion boxes or pixel masks. Its description reports 84,012 images across several institutions/clinics. | The Zenodo file API currently lists a label spreadsheet and `CHARDI_test.zip` (about 14.6 GB), not a complete training bundle. | **Not a detection dataset.** Could support multi-label classification or source/domain robustness if the complete train set and terms are confirmed. Labels were extracted from reports using NLP/rules and are not equivalent to radiologist-localized boxes. |

### Important distinctions

“Detection” is used loosely in dataset descriptions. For this project it should
mean image-level **bounding-box localization**, not just an image label.
VinDr-CXR supplies actual 2D finding boxes. ULS23 and MAGIC-CT are primarily
3D segmentation/localization resources, and IMA++ supplies 2D masks. CRADI
supplies image-level labels only.

## Compact paper shortlist

The following shortlist prioritizes 2D chest radiographs and localized
abnormalities, while keeping the first experiment small. ChestX-Det10 and
RSNA are present locally and have native box annotations. SIIM-ACR is not a
usable third dataset at present: its official bundle lacks the original
training images, and the local archive also fails ZIP integrity/listing
checks. For a valid SIIM source, turning RLE masks into boxes would be
scripted preprocessing, not manual annotation. This is a shortlist for staged
evaluation, not a recommendation to merge all labels or train on all three at
once.

| Role | Dataset | Scale and annotations | Download/access caveat |
|---|---|---|---|
| Primary, compact baseline | [ChestX-Det10](https://github.com/Deepwise-AILab/ChestX-Det10-Dataset) | 3,543 images; native bounding boxes for 10 thoracic abnormality classes; JSON annotations with supplied train/test splits. | Published image archives are 1,210,114,616 and 218,238,743 bytes, about 1.43 GB combined. This is the best first pilot for a multi-class detector. |
| Candidate comparison | [RSNA Pneumonia Detection Challenge](https://www.rsna.org/artificial-intelligence/ai-image-challenge/rsna-pneumonia-detection-challenge-2018) / [Kaggle data](https://www.kaggle.com/competitions/rsna-pneumonia-detection-challenge/data) | 26,684 training chest radiographs with pneumonia localization boxes; one target finding, so it complements rather than duplicates ChestX-Det10's multi-class task. | Downloaded as a 3,932,287,530-byte Stage 2 archive, kept zipped, and passed ZIP integrity verification. The archive includes 3,000 unlabeled test images. See the local dataset `README.txt` for its SHA-256 and terms caveat. Kaggle account/rules are required. |
| Incomplete until training images are sourced | [SIIM-ACR Pneumothorax Segmentation](https://www.kaggle.com/competitions/siim-acr-pneumothorax-segmentation/data) | The official Kaggle record lists 3,209 files totaling 439.11 MB. It provides stage-2 test images and RLE annotations; its instructions say the training images were hosted in Google Cloud Healthcare, which the page now says is no longer available. | The local 328 MiB ZIP has no readable central directory; `unzip -t` fails. It is not a verified usable archive. The record links a community Kaggle mirror, [seesee/siim-train-test](https://www.kaggle.com/datasets/seesee/siim-train-test), but its availability, completeness, and terms still need verification. If a complete mirror is available, masks are already annotated and boxes could be derived by script; no manual annotation is needed. |

For a first **box-detection pilot**, ChestX-Det10 is the clearest quick-start.
RSNA is the second local native-box dataset and is large but manageable for
the local storage budget. Do not count SIIM-ACR as a third training dataset
until a complete archive and authorized image source are verified. A paper
that only runs standard detectors independently on ChestX-Det10 and RSNA
would be a baseline study, not yet a compelling novel contribution. A
stronger candidate question is cross-dataset localization under ontology and
annotation shift, but it requires a careful common-finding map and a suitable
external dataset such as VinDr-CXR; do not assume similarly named labels are
equivalent.

## Local inventory and annotation audit

The local medical folder currently contains notes, dataset documentation,
annotations, and archives, but no detector package or training code. It is
not a Git repository yet. The existing `.gitignore` excludes `.env`,
`.env.*`, and `datasets/**` while allowing dataset README files through; keep
those protections. The `.env` file was not opened.

| Dataset | Verified local facts | Readiness |
|---|---|---|
| ChestX-Det10 | Train/test JSON has 3,001/542 records, 6,863/1,476 boxes, and all 10 classes in both splits. There are 681/83 records without boxes. All rows have matching `syms`/`boxes` lengths; coordinates are finite 4-tuples with positive area and non-negative origins. | Ready for a parser/rendering pilot. Still verify coordinates against decoded image dimensions and inspect rendered overlays before training. |
| RSNA Pneumonia | The archive contains the training labels CSV. It has 30,227 label rows: 9,555 positive box rows across 6,012 positive images and 20,672 negative rows. All positive rows have numeric, non-negative origins and positive width/height. The Stage 2 archive was previously verified for ZIP integrity; the 3,000 test images are unlabeled. | Ready for a separate pneumonia-detection baseline, subject to Kaggle terms and patient-grouped train/validation partitioning. |
| SIIM-ACR Pneumothorax | The local 328 MiB file is named as a ZIP but has no readable central directory; `unzip -t` and member listing fail. Its SHA-256 is `9438df8d437892d4e2cfc744587800bef415ec83260645b55e54de7dbf855e27`. | Not usable as-is. Do not extract, train, or rely on it until a complete authorized source is obtained and verified. |

These checks validate annotation structure, not clinical correctness,
annotation quality, or complete correspondence between annotations and
images. The research code should repeat these checks as automated data
preflight tests rather than relying on this one-time inventory.

To keep the work tractable, first run one detector and a fixed training recipe
on ChestX-Det10. Then decide whether RSNA and SIIM-ACR are separate
dataset-specific experiments or whether the paper needs a narrower common
target. Keep their official splits where available, report per-class AP and
the class support, and avoid claiming a universal medical detector from
performance on only one small dataset. Dataset size alone does not ensure
good results; class imbalance, box quality, and the evaluation split matter.

## Zenodo API and safe download pattern

Zenodo has a REST API for searching records, reading record/file metadata, and
retrieving file content. Public record metadata and a public file endpoint were
checked anonymously and returned HTTP 200. The API exposes each file's exact
key, byte size, checksum, and content URL. Upload/deposit operations use an
access token; public read/download endpoints worked without one in these
checks. A token does not bypass a record's data-use restrictions.

Inspect metadata before transferring a large archive:

```bash
curl -fsSL 'https://zenodo.org/api/records/12721389?prettyprint=1' |
  jq '{id, title, license: .metadata.license.id,
       files: [.files[] | {key, size, checksum, url: .links.self}]}'
```

Download one explicitly chosen file with resume support, then verify the
checksum published by the API:

```bash
curl -fL --retry 3 -C - \
  -o vindr_test.zip \
  'https://zenodo.org/api/records/12721389/files/vindr_test.zip/content'

md5 -q vindr_test.zip
# Expected on macOS: 76023bf3d1dee12dbb4c300e5ce6f9ae
# On Linux, use: echo '76023bf3d1dee12dbb4c300e5ce6f9ae  vindr_test.zip' | md5sum -c -
```

Pin the record/version and keep a small manifest of DOI, file names, sizes,
checksums, download date, source URL, license, and citation. Do not put medical
images, annotation exports, access tokens, or restricted records in GitHub.
For restricted records, use the actual application/DUA route; do not automate
around it.

## Suggested feasibility sequence

1. **Choose the paper question before selecting models.** A plain detector
   comparison on ChestX-Det10 and RSNA is useful engineering, but is not by
   itself a strong novelty claim. If the goal is cross-dataset generalization,
   first validate a defensible shared-label map and access to an external
   dataset such as VinDr-CXR.
2. **Treat ChestX-Det10 as the first pilot.** Implement its parser and
   preflight checks, visualize boxes on decoded images, confirm split
   integrity, and establish a reproducible baseline without touching the
   official test split for tuning.
3. **Add RSNA as a separate adapter and task.** Preserve its official test
   boundary, create validation groups by patient, and report its metric and
   protocol separately from ChestX-Det10.
4. **Resolve SIIM provenance before implementation.** Obtain a complete
   archive/image source with authorized access, then validate the RLE masks
   before adding that adapter.
5. **Build modularly around a canonical sample/box schema.** Keep dataset
   adapters, PNG/DICOM decoding, ontology mappings, split checks, models,
   training, and dataset-specific metrics isolated. Add parser tests using
   synthetic fixtures, and store runs/checkpoints outside version control.
6. **Check total bytes, terms, and access requirements** for each selected
   download before transferring it. Keep the aggregate within the chosen
   storage/time budget; skip VinDr-CXR if a roughly 48 GB download is too large.
7. **Run a small fixed baseline, then expand only if it supports the paper's
   question.** Keep dataset-specific splits and results separate; report
   per-class localization metrics and avoid treating different label
   definitions as interchangeable.

ChestX-Det10 and RSNA are present locally and ignored by the medical
project's `.gitignore`; the RSNA archive remains zipped. The local SIIM
archive is unreadable and not a usable training set. No Zenodo token or
account is needed for the public metadata checks above. A decision about the
paper question and data-use terms should precede training or any further
multi-gigabyte download.

## Sources

- [VinDr-CXR Zenodo record](https://zenodo.org/records/12721389) and [official PhysioNet description](https://physionet.org/content/vindr-cxr/1.0.0/)
- [MAGIC-CT v2 Zenodo record and DUA](https://zenodo.org/records/18389015)
- [ULS23 challenge](https://uls23.grand-challenge.org/) and [Zenodo Part 2](https://zenodo.org/records/10050960) / [Part 3](https://zenodo.org/records/10054306)
- [IMA++ Zenodo record](https://zenodo.org/records/14201693)
- [CRADI Zenodo record](https://zenodo.org/records/5493595)
- [RSNA Pneumonia Detection Challenge](https://www.rsna.org/artificial-intelligence/ai-image-challenge/rsna-pneumonia-detection-challenge-2018)
- [SIIM-ACR Pneumothorax Segmentation on Kaggle](https://www.kaggle.com/competitions/siim-acr-pneumothorax-segmentation)
- [ChestX-Det10 dataset repository](https://github.com/Deepwise-AILab/ChestX-Det10-Dataset)
- [Zenodo REST API documentation](https://developers.zenodo.org/)

## Research and architecture preparation

The recommended detection study scope and evaluation safeguards are
documented in [`docs/research_findings.md`](docs/research_findings.md) and
[`docs/detection_workflow.md`](docs/detection_workflow.md). The package design
is intentionally broader than a single dataset: it uses registries,
task-specific contracts, composable transformations, and validated
configuration/CLI routing for adding datasets and models independently; see
[`docs/architecture_blueprint.md`](docs/architecture_blueprint.md). ChestX-Det10
is the first validation pilot, not the entire codebase's scope. The research
phase did not authorize uploading or training on local archives.

The implementation now has a prepare-first data path: raw dataset adapters
materialize versioned artifacts under ignored `processed_data/`, and the
training-facing reader loads only those artifacts. See the project
[`README.md`](README.md) for the current ChestX-Det10 preparation command and
the [`architecture blueprint`](docs/architecture_blueprint.md) for the
extensible lifecycle.
