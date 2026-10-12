# Project Problem Definition

**Status:** Provisional research brief; not a novelty claim or a frozen
protocol.
**Last reviewed:** 2026-10-12
**Decision gate:** Complete the literature review and confirm data access and
readiness before selecting a paper question or training models.

## Working topic

**How do annotation type and dataset shift affect localization learning and
evaluation in chest radiographs?**

This is the proposed overarching research programme, not yet an approved
single-paper title or a novelty claim. Its scientific core is localization
under different forms of radiologist supervision—not building a modular
codebase and not comparing unrelated leaderboard scores.

The three datasets can contribute to a connected programme, but they do not
currently support one ordinary pooled benchmark experiment:

- ChestX-Det10 supplies multi-finding bounding boxes, including
  pneumothorax.
- RSNA supplies boxes for possible lung opacity, a distinct target that
  should not be relabeled as pneumothorax or ChestX-Det10 consolidation.
- SIIM-ACR supplies pneumothorax masks, which are not equivalent to boxes.
  Its local archive is currently unusable.

**Best single-paper hypothesis, conditional on a new reader study:** measure
whether model-to-reference localization error is meaningfully different
from qualified-reader-to-reader disagreement, and whether that relationship
varies across task-specific case studies. This could use all three datasets
as separate analyses, never as a pooled score. Since dataset, cohort,
finding, and annotation geometry differ together, between-dataset differences
must be interpreted descriptively, not attributed to annotation geometry
alone. The study requires blinded, independent radiologist rereads and a
complete authorized SIIM source; neither condition is currently established.

**Best feasible alternative if rereads are not possible:** a focused
pneumothorax box-to-mask transfer study using ChestX-Det10 and SIIM-ACR after
SIIM recovery. RSNA then belongs in a separate possible-opacity study, not
that paper. A project or thesis may still connect all three as separate
studies, provided each claim and metric remains dataset/task-specific.

## Problem statement

Chest-radiograph datasets with ready-made annotations do not necessarily
define the same prediction problem. The local resources include multi-class
finding boxes, possible-pneumonia opacity boxes, and pneumothorax masks.
They differ in image format, annotation semantics, access/readiness, and
evaluation protocol. Their scores are not commensurate. ChestX-Det10 and
RSNA also have NIH ChestX-ray data lineage in their dataset descriptions, so
image/patient overlap is a concrete leakage risk to investigate; overlap
between these particular local subsets has **not** been established.
Treating the datasets as interchangeable, or pooling them without evidence,
could make results difficult to interpret and create invalid
generalization claims.

The engineering problem is to support each source through a tested
prepare-first adapter and a task-specific evaluation path. The research
problem is still open: we must identify a question that is both supported by
the usable data and meaningfully extends prior work. A modular codebase or a
new baseline alone is not a scientific novelty claim.

## Proposed scientific question and decision

> When localization models are evaluated against radiologist annotations,
> how much of the observed model-to-reference disagreement exceeds
> qualified-reader disagreement, and how does that relationship differ
> across box-annotated findings and mask-annotated pneumothorax?

This is the strongest current **single-paper concept** for including all
three resources: its common scientific object is localization agreement
relative to human annotation, not a shared disease label or metric. The
primary analysis would estimate reader-to-reader and model-to-reader
agreement on the same held-out images using blinded independent rereads.
Model predictions must be frozen before reread labels are revealed, and the
rereading radiologists must not see the source annotations or predictions.
ChestX-Det10, RSNA, and SIIM would each be analyzed under their own
instructions, reference format, and native evaluation; scores such as
fixed-FP recall, mAP, and Dice must not be averaged or presented as directly
comparable. Because finding, cohort, and annotation geometry are not
independently varied across these datasets, between-dataset differences
cannot establish that annotation geometry caused a difference.

The hypothesis is testable, but its feasibility is **not yet demonstrated**:
the public ChestX-Det10 and RSNA releases do not by themselves provide usable
independent reader annotations for every case, a reread protocol and reader
resources are not yet arranged, and the local SIIM archive is incomplete.
Therefore this is a research proposal, not an approved paper topic. Do not
start training for it until the three feasibility gates pass:

1. Confirm permission, funding, and a blinded protocol for independent
   radiologist rereads on samples from each dataset.
2. Recover a complete authorized SIIM source and validate images, masks,
   labels, and patient/study grouping.
3. Finish targeted prior-art review and a cross-dataset duplicate audit;
   determine that the reader-relative question is not already answered by
   closely related work.

If these gates fail, do not dilute the question to force all three datasets
into one paper. Use a pneumothorax box-to-mask transfer study on
ChestX-Det10 and SIIM only if SIIM becomes usable and a targeted novelty
review supports it. Otherwise run a separate RSNA possible-opacity study or
keep the work as a rigorous engineering/reproducibility baseline. Never
equate RSNA opacity with ChestX-Det10 consolidation without a separately
justified clinical mapping.

## Closest prior work and implications

The annotated bibliography below is a focused literature map, not a
systematic review. The rest of the bibliography provides methodological
foundations; it does not establish novelty for our exact proposed study.

### Reading depth and scope

The direct-precedent assessment draws on the ChestX-Det10 dataset paper and
challenge paper, their released evaluator, the full RSNA annotation article,
the full Zech et al. external-validation article, and Dumbrique et al.'s
SIIM-ACR study. The remaining
numbered works were screened and annotated for relevance from their
publication records and accessible abstracts/source summaries; **they have
not all been independently read cover-to-cover**. Reporting guidelines and
general detector/segmentation papers below are foundations, not direct
evidence about the exact local datasets or proposed sensitivity question.

Before a final paper proposal, read the methods, results, limitations, and
supplementary material of every closest task-specific paper identified in a
targeted search. Record the exact claim, data version/split, metric,
comparator, result, and limitation in a study matrix. This focused source
review is not proof that no related paper exists.

| Closest source | What the paper/source establishes | Implication for topic selection |
|---|---|---|
| Liu, Lian & Yu (2020), [ChestX-Det10 paper](https://arxiv.org/abs/2006.10550v3) | Introduces expert box annotations for ten findings on an NIH ChestX-ray14 subset; describes the 3,001/542 split and a Faster R-CNN/FPN baseline; reports AP and fixed-FP recall. | Dataset, task, conventional baseline, and reporting both endpoint families are prior work. Another baseline or simple AP-versus-recall table is weak novelty. |
| Lian et al. (2020), [ChestX-Det10 challenge results](https://arxiv.org/abs/2010.10298v2) | Reports six second-round challenge teams, detector designs and augmentation strategies, using native recall at 0.05/0.1/0.2 FP per image with IoU 0.5. | A detector leaderboard is established; any new comparison needs a different, consequential hypothesis. |
| [ChestX-Det10 official evaluator](https://github.com/Deepwise-AILab/ChestX-Det10-Dataset/blob/master/eval.py) | Defines FROC-style matching/interpolation at the native FP/image points; the released IoU implementation uses inclusive `+1` box dimensions. | Reimplementing a scorer is not a contribution by itself. First identify a documented ambiguity/bug and quantify whether it changes conclusions. |
| Shih et al. (2019), [RSNA annotation paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC8017407/) and [DOI](https://doi.org/10.1148/ryai.2019180041) | Describes expert annotation of opacities that may represent pneumonia, including multiple readers/adjudication, as a distinct NIH-derived challenge task. | RSNA is not a ChestX-Det10 class and cannot be pooled as a matching ontology. Use its own patient grouping and mAP at IoU 0.4. |
| Zech et al. (2018), [institutional generalization study](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002683) | In 158,323 radiographs from NIH, Mount Sinai, and Indiana, external performance was lower in 3 of 5 natural comparisons; hospital source was highly predictable, and prevalence differences affected apparent performance. The endpoint was image-level pneumonia screening/classification. | Motivates caution and source-aware design, but does not test these box datasets, local subsets, or actual ChestX-Det10/RSNA overlap. |
| Wang et al. (2020), [CheXLocNet](https://doi.org/10.1371/journal.pone.0242013) | Studies automatic pneumothorax localization in chest radiographs, including SIIM-ACR-derived data and segmentation/localization evaluation. | Pneumothorax localization on SIIM is established prior work; a new model or standard segmentation baseline is not enough. |
| Santomartino et al. (2023), [code-free CXR study](https://doi.org/10.1148/ryai.220062) | Evaluates code-free deep-learning systems across chest-radiograph classification, object detection, and segmentation; includes external benchmark tasks such as RSNA opacity detection and SIIM pneumothorax segmentation. | Multi-benchmark use already exists, but it does not make unlike targets or native metrics interchangeable, nor does it answer reader-relative localization agreement. |
| Dumbrique et al. (2024), [P-DeSeRay](https://doi.org/10.3389/fradi.2024.1424065) | Evaluates pneumothorax detection/segmentation on SIIM-ACR and a private hospital dataset and reports a loss ablation. | Routine SIIM architecture/loss comparisons already have direct precedent. SIIM is a separate segmentation task and unusable from the current local archive. |

### Topic comparison and scope decision

| Candidate | Scientific question and use of datasets | Feasibility and decision |
|---|---|---|
| **A. Model localization versus reader variability (recommended all-three paper concept)** | On blinded rereads, compare model-to-reader localization with reader-to-reader agreement. Use ChestX-Det10 findings boxes, RSNA possible-opacity boxes, and SIIM pneumothorax masks as separate task-specific analyses. | Strongest shared scientific question without pretending labels or metrics match. Not currently executable: requires new independent reads and a valid SIIM source. Select only if reader resources, permissions, dataset readiness, and novelty checks pass. |
| **B. Pneumothorax box-to-mask transfer** | Test whether box supervision from ChestX-Det10 can support pneumothorax mask localization on SIIM (and/or the reverse direction), comparing with target-only baselines and reporting native metrics separately. | More concrete and task-linked, but only uses two datasets and SIIM is blocked. Target mapping, patient/image deduplication, and novelty need careful review. RSNA remains separate. |
| **C. Heterogeneous multi-task learning** | Share an encoder while using dataset-specific heads for ChestX-Det10 boxes, RSNA opacity boxes, and SIIM masks; compare against independently trained and target-only models. | Plausible programme direction but not selected as a paper: requires full SIIM, adequate compute, leakage controls, and a sharper causal hypothesis than “joint training helps.” Negative transfer is a central possible result. |
| **D. ChestX-Det10 evaluator or RSNA rendering sensitivity** | Test a specific consequential matching/interpolation ambiguity or DICOM-rendering choice using frozen predictions and the dataset-native protocol. | Useful correctness/pilot work. It becomes a paper only if targeted review finds a consequential unresolved choice; routine metric reporting or rendering ablations are not enough. Keep each dataset's task separate. |
| **E. Three-dataset model leaderboard** | Train standard detectors/segmenters and list scores for each dataset. | Rejected as a paper topic: unrelated targets, output geometry, and metrics do not become one scientific question by sharing an architecture. |

**Decision:** advance candidate A as the lead *proposal* for a unified
three-dataset paper, but do not call it novel or begin its training until
feasibility and prior-art gates pass. If reader rereads cannot be arranged,
prefer candidate B as a two-dataset pneumothorax study only after SIIM is
recovered. The larger project may still include a separate RSNA study. A
three-dataset thesis/programme is defensible as connected studies; one
three-dataset paper is defensible only if it tests a shared scientific
hypothesis such as reader-relative localization and preserves task-specific
analyses.

## Annotated literature review: 57 publications

This focused review includes 57 distinct research papers, dataset/challenge
papers, methods papers, reviews, and reporting/methodology publications. It
is not a systematic review and does not claim exhaustive coverage. Brief
findings explain relevance; follow the linked source for detailed methods,
cohort details, exact metrics, and full author metadata. General detector
and methods papers provide foundations, not evidence of performance on our
datasets.

### A. Dataset, cohort, and annotation provenance

1. **Wang et al. (2017), “ChestX-ray8: Hospital-scale Chest X-ray Database and Benchmarks on Weakly-Supervised Classification and Localization of Common Thorax Diseases.”** Dataset/benchmark. [DOI](https://doi.org/10.1109/CVPR.2017.369)
   Introduces the NIH chest-radiograph collection and weak-label classification/localization benchmarks. It is relevant to source lineage and to distinguishing report-derived labels from instance-level box ground truth.

2. **Liu, Lian & Yu (2020), “ChestX-Det10: Chest X-ray Dataset on Detection of Thoracic Abnormalities.”** Dataset paper. [arXiv:2006.10550](https://arxiv.org/abs/2006.10550)
   Introduces radiologist box annotations for ten abnormality categories on an NIH ChestX-ray14 subset. This is the primary source for the task and annotation definition.

3. **Liu et al. (2020), “The Detection of Thoracic Abnormalities ChestX-Det10 Challenge Results.”** Challenge paper. [arXiv:2010.10298](https://arxiv.org/abs/2010.10298)
   Reports challenge systems and results on ChestX-Det10. It rules out treating a routine re-run of conventional detectors as automatically novel.

4. **Irvin et al. (2019), “CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Comparison.”** Dataset/benchmark. [DOI](https://doi.org/10.1609/aaai.v33i01.3301590)
   Presents report-derived labels with explicit uncertainty and expert comparison. It motivates preserving uncertainty and label provenance rather than converting weak labels into localization targets.

5. **Johnson et al. (2019), “MIMIC-CXR, a de-identified publicly available database of chest radiographs with free-text reports.”** Dataset paper. [DOI](https://doi.org/10.1038/s41597-019-0322-0)
   Describes a large clinical CXR cohort with reports. Its provenance and cohort characteristics matter when interpreting transportability and external validation.

6. **Bustos et al. (2020), “PadChest: A large chest X-ray image dataset with multi-label annotated reports.”** Dataset paper. [DOI](https://doi.org/10.1016/j.media.2020.101797)
   Presents a large multi-label report-annotated collection. It supplies useful label context, but not box or mask supervision unless a specific annotation explicitly provides it.

7. **Nguyen et al. (2022), “VinDr-CXR: An open dataset of chest X-rays with radiologist’s annotations.”** Dataset paper. [DOI](https://doi.org/10.1038/s41597-022-01498-2)
   Describes radiologist-annotated CXR, including localized findings. It is a possible later localization/external dataset, subject to its cohort and reader-protocol differences.

8. **Demner-Fushman et al. (2016), “Preparing a collection of radiology examinations for distribution and retrieval.”** Dataset paper. [DOI](https://doi.org/10.1016/j.jbi.2015.11.023)
   Describes curation of a radiology image/report collection. It is relevant to release construction, provenance, and why annotations must be understood in the context of their source.

9. **Wu et al. (2021), “Chest ImaGenome Dataset for Clinical Reasoning.”** Dataset paper. [arXiv:2108.00316](https://arxiv.org/abs/2108.00316)
   Introduces structured anatomical and semantic annotations linked to CXR and reports. It reinforces the distinction between anatomy, finding labels, and localization targets.

10. **Boecking et al. (2022), “Making the Most of Text Semantics to Improve Biomedical Vision–Language Processing.”** Primary study/dataset contribution. [DOI](https://doi.org/10.1007/978-3-031-20059-5_1); [arXiv](https://arxiv.org/abs/2204.09817)
    Studies semantic vision-language learning and radiologist phrase-grounding annotations used by MS-CXR. Phrase grounding is related to, but not identical with, fixed-category object detection.

11. **Lakhani et al. (2023), “The 2021 SIIM-FISABIO-RSNA Machine Learning COVID-19 Challenge: Annotation and Standard Exam Classification of COVID-19 Chest Radiographs.”** Challenge/dataset paper. [DOI](https://doi.org/10.1007/s10278-022-00706-8)
    Documents curation and annotation for a different CXR challenge. It is a useful annotation-protocol reference, not a SIIM-ACR pneumothorax study.

### B. CXR classification, localization, and clinical comparison

12. **Rajpurkar et al. (2017), “CheXNet: Radiologist-Level Pneumonia Detection on Chest X-Rays with Deep Learning.”** Primary study/preprint. [arXiv:1711.05225](https://arxiv.org/abs/1711.05225)
    Presents pneumonia classification on image-level labels and a radiologist comparison. It is not evidence of bounding-box localization performance.

13. **Rajpurkar et al. (2018), “Deep learning for chest radiograph diagnosis: A retrospective comparison of the CheXNeXt algorithm to practicing radiologists.”** Primary study. [DOI](https://doi.org/10.1371/journal.pmed.1002686)
    Compares a multi-finding algorithm with radiologists retrospectively. Its classification endpoint should not be compared directly with box or mask metrics.

14. **Yao et al. (2017), “Learning to Diagnose from Scratch by Exploiting Dependencies among Labels.”** Primary study/preprint. [arXiv:1710.10501](https://arxiv.org/abs/1710.10501)
    Models co-occurrence/dependency among thoracic disease labels. It informs within-dataset multi-label learning but does not justify merging unrelated dataset ontologies.

15. **Baltruschat et al. (2019), “Comparison of deep learning approaches for multi-label chest X-ray classification.”** Primary study. [DOI](https://doi.org/10.1038/s41598-019-42294-8)
    Compares multi-label CXR classification approaches. It motivates controlled baseline comparisons while keeping classification metrics separate from localization.

16. **Li et al. (2018), “Thoracic Disease Identification and Localization with Limited Supervision.”** Primary study. [arXiv:1711.06373](https://arxiv.org/abs/1711.06373)
    Combines image labels and limited localization supervision. It is relevant to weakly supervised alternatives, but such localization must be compared against real box ground truth carefully.

17. **Guan et al. (2018), “Diagnose Like a Radiologist: Attention Guided Convolutional Neural Network for Thorax Disease Classification.”** Primary study/preprint. [arXiv:1801.09927](https://arxiv.org/abs/1801.09927)
    Uses attention-guided features for CXR classification. Attention visualizations are not validated boxes or masks without a localization evaluation.

### C. Detection, segmentation, and localization methods

18. **Ren et al. (2015), “Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks.”** Methods paper. [DOI](https://doi.org/10.1109/TPAMI.2016.2577031)
    Introduces a two-stage detector and provides a conventional reproducible baseline family for box tasks.

19. **Lin et al. (2017), “Feature Pyramid Networks for Object Detection.”** Methods paper. [DOI](https://doi.org/10.1109/CVPR.2017.106)
    Presents multiscale features for detection. It motivates documenting input scaling and evaluating small-finding behavior.

20. **Lin et al. (2017), “Focal Loss for Dense Object Detection.”** Methods paper. [DOI](https://doi.org/10.1109/ICCV.2017.324)
    Introduces focal loss for foreground/background imbalance. It is a possible detector baseline component, not a substitute for native metric reporting.

21. **He et al. (2017), “Mask R-CNN.”** Methods paper. [DOI](https://doi.org/10.1109/ICCV.2017.322)
    Extends detection with instance masks. It is relevant if SIIM data become available, while preserving SIIM as segmentation rather than converting its task implicitly.

22. **Redmon & Farhadi (2018), “YOLOv3: An Incremental Improvement.”** Methods preprint. [arXiv:1804.02767](https://arxiv.org/abs/1804.02767)
    Describes a one-stage, multiscale detector. It offers a contrasting family only if the benchmark fixes training and evaluation conditions.

23. **Ronneberger et al. (2015), “U-Net: Convolutional Networks for Biomedical Image Segmentation.”** Methods paper. [DOI](https://doi.org/10.1007/978-3-319-24574-4_28)
    Introduces an encoder-decoder segmentation architecture and is a reasonable SIIM starting baseline if valid images and masks are recovered.

24. **Milletari et al. (2016), “V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation.”** Methods paper. [DOI](https://doi.org/10.1109/3DV.2016.79)
    Presents volumetric segmentation and a Dice-based objective. It informs loss choices but is not necessarily an appropriate 2D CXR architecture.

25. **Oktay et al. (2018), “Attention U-Net: Learning Where to Look for the Pancreas.”** Methods preprint. [arXiv:1804.03999](https://arxiv.org/abs/1804.03999)
    Adds attention gates to U-Net. Transfer to pneumothorax masks would need direct validation and should not be assumed beneficial.

26. **Zhou et al. (2018), “UNet++: A Nested U-Net Architecture for Medical Image Segmentation.”** Methods paper. [DOI](https://doi.org/10.1109/TMI.2018.2848986)
    Proposes nested skip pathways. It is a possible controlled SIIM comparator, not an automatic choice.

27. **Chen et al. (2018), “Encoder-Decoder with Atrous Separable Convolution for Semantic Image Segmentation.”** Methods paper. [DOI](https://doi.org/10.1109/TPAMI.2018.2844175)
    Presents DeepLabv3+. It supplies another segmentation baseline family if SIIM's task becomes feasible.

28. **Isensee et al. (2021), “nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation.”** Methods paper. [DOI](https://doi.org/10.1038/s41592-020-01008-z)
    Demonstrates the strength of carefully configured preprocessing and training. It supports strong baselines and disciplined pipeline documentation over architecture novelty alone.

29. **Sudre et al. (2017), “Generalised Dice Overlap as a Deep Learning Loss Function for Highly Unbalanced Segmentations.”** Methods paper/preprint. [arXiv:1707.03237](https://arxiv.org/abs/1707.03237)
    Proposes generalized Dice loss for class imbalance. It may inform a segmentation ablation, but loss choice must remain distinct from the official score.

30. **Kervadec et al. (2019), “Boundary loss for highly unbalanced segmentation.”** Methods paper/preprint. [arXiv:1812.07032](https://arxiv.org/abs/1812.07032)
    Introduces a boundary-aware loss. Consider only if mask boundary quality and the scientific question justify it.

31. **Selvaraju et al. (2017), “Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization.”** Methods paper. [DOI](https://doi.org/10.1109/ICCV.2017.74)
    Introduces class activation visualizations. It can support qualitative inspection but does not replace detector outputs or segmentation masks.

32. **Adebayo et al. (2018), “Sanity Checks for Saliency Maps.”** Methods paper. [arXiv:1810.03292](https://arxiv.org/abs/1810.03292)
    Shows that some saliency methods fail parameter/data randomization checks. If explanations are included, visual plausibility alone is insufficient evidence.

### D. Generalization, shortcuts, subgroup performance, and leakage

33. **Zech et al. (2018), “Variable generalization performance of a deep learning model to detect pneumonia in chest radiographs: A cross-sectional study.”** Primary study. [DOI](https://doi.org/10.1371/journal.pmed.1002683)
    Finds variation in pneumonia-model performance across institutions. It motivates external evaluation, but these datasets alone do not establish transportability.

34. **Oakden-Rayner et al. (2020), “Hidden stratification causes clinically meaningful failures in machine learning for medical imaging.”** Primary/methodological study. [DOI](https://doi.org/10.1038/s42256-020-0168-1)
    Shows aggregate labels and metrics can conceal important subgroups. It supports per-class and supported error analyses rather than relying on one mean score.

35. **DeGrave et al. (2021), “AI for radiographic COVID-19 detection selects shortcuts over signal.”** Primary study. [DOI](https://doi.org/10.1038/s42256-021-00338-7)
    Demonstrates shortcut learning in radiographs. It motivates checking acquisition, source, processing, and annotation artifacts.

36. **Seyyed-Kalantari et al. (2021), “Underdiagnosis bias of artificial intelligence algorithms applied to chest radiographs in under-served patient populations.”** Primary study. [DOI](https://doi.org/10.1038/s41591-021-01595-0)
    Reports underdiagnosis disparities in CXR algorithms. Subgroup analyses require suitable metadata, support, and appropriate governance.

37. **Larrazabal et al. (2020), “Gender imbalance in medical imaging datasets produces biased classifiers for computer-aided diagnosis.”** Primary study. [DOI](https://doi.org/10.1038/s41467-020-17971-2)
    Studies effects of demographic imbalance on classifier behavior. It motivates cohort-description and subgroup caution where permissible metadata exist.

38. **Roberts et al. (2021), “Common pitfalls and recommendations for using machine learning to detect and prognosticate for COVID-19 using chest radiographs and CT scans.”** Review/methodology. [DOI](https://doi.org/10.1038/s42256-021-00307-0)
    Summarizes leakage and validation pitfalls in imaging ML. It supports careful split design and restrained interpretation.

39. **Subbaswamy & Saria (2020), “From development to deployment: dataset shift, causality, and shift-stable models in health AI.”** Methods/review. [DOI](https://doi.org/10.1093/biostatistics/kxz041)
    Frames dataset shift and causal structure as central to transportability. It motivates auditing cohort provenance before calling another set an external test.

40. **Varoquaux & Cheplygina (2022), “Machine learning for medical imaging: methodological failures and recommendations for the future.”** Review/methodology. [DOI](https://doi.org/10.1038/s41746-022-00592-y)
    Reviews recurring methodological weaknesses in medical imaging ML and recommends stronger validation and reproducibility.

41. **Kapoor & Narayanan (2023), “Leakage and the reproducibility crisis in machine-learning-based science.”** Methodological paper. [DOI](https://doi.org/10.1016/j.patter.2023.100804)
    Explains how leakage can inflate findings. It supports auditing patient-, image-, and duplicate-level separation and documenting preprocessing.

42. **Wynants et al. (2020), “Prediction models for diagnosis and prognosis of COVID-19: systematic review and critical appraisal.”** Systematic review. [DOI](https://doi.org/10.1136/bmj.m1328)
    Identifies bias and validation weaknesses in prediction-model studies. Though COVID-focused, its appraisal lessons inform study design.

43. **Kelly et al. (2019), “Key challenges for delivering clinical impact with artificial intelligence.”** Review/perspective. [DOI](https://doi.org/10.1186/s12916-019-1426-2)
    Discusses the gap between technical performance and clinical impact. It supports limiting our claims to retrospective technical evidence.

### E. Metrics, evaluation, calibration, and reporting

44. **Lin et al. (2014), “Microsoft COCO: Common Objects in Context.”** Dataset/metric paper. [DOI](https://doi.org/10.1109/CVPR.2014.471)
    Establishes widely used object-detection AP conventions. Those conventions do not replace dataset-native ChestX-Det10 or RSNA protocols.

45. **Taha & Hanbury (2015), “Metrics for evaluating 3D medical image segmentation: analysis, selection, and tool.”** Methods paper. [DOI](https://doi.org/10.1186/s12880-015-0068-x)
    Analyzes segmentation metrics including overlap measures. It supports explicit Dice definitions and interpretation caveats for sparse masks.

46. **Udupa et al. (2006), “A framework for evaluating image segmentation algorithms.”** Methods paper. [DOI](https://doi.org/10.1109/TMI.2006.876837)
    Discusses principled segmentation evaluation. It motivates reporting error types and boundary behavior beyond a single overlap score.

47. **Guo et al. (2017), “On Calibration of Modern Neural Networks.”** Methods paper. [PMLR](https://proceedings.mlr.press/v70/guo17a.html)
    Studies confidence calibration. It is relevant when confidence thresholds are selected to meet fixed false-positive operating points.

48. **Van Calster et al. (2019), “Calibration: the Achilles heel of predictive analytics.”** Methodological paper. [DOI](https://doi.org/10.1186/s12916-019-1466-7)
    Argues calibration matters for interpreting predicted risk. Detection confidence still requires task-specific operating-point evaluation.

49. **Collins et al. (2024), “TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods.”** Reporting guideline. [DOI](https://doi.org/10.1136/bmj-2023-078378)
    Provides updated reporting guidance for prediction models. Use it as a complement, not a replacement, for imaging-specific reporting.

50. **Mongan et al. (2020), “Checklist for Artificial Intelligence in Medical Imaging (CLAIM): A Guide for Authors and Reviewers.”** Reporting guideline. [DOI](https://doi.org/10.1148/ryai.2020200029)
    Gives imaging-specific reporting recommendations. It is directly useful for documenting decoding, preprocessing, partitions, reference standards, and reproducibility.

51. **Liu et al. (2020), “Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: the CONSORT-AI extension.”** Reporting guideline. [DOI](https://doi.org/10.1038/s41591-020-1034-x)
    Extends trial reporting for AI interventions. It is mainly relevant if this research later reaches clinical trials, not as a requirement for retrospective benchmarking.

52. **Cruz Rivera et al. (2020), “Guidelines for clinical trial protocols for interventions involving artificial intelligence: the SPIRIT-AI extension.”** Reporting guideline. [DOI](https://doi.org/10.1038/s41591-020-1037-7)
    Extends protocol guidance for AI clinical trials. It is useful for future prospective protocol design, not a substitute for a benchmark protocol.

53. **Vasey et al. (2022), “Reporting guideline for the early-stage clinical evaluation of decision support systems driven by artificial intelligence: DECIDE-AI.”** Reporting guideline. [DOI](https://doi.org/10.1038/s41591-022-01772-9)
    Guides early-stage clinical evaluation of decision support. It matters only if the study evaluates human interaction or workflow.

54. **Wolff et al. (2019), “PROBAST: A Tool to Assess the Risk of Bias and Applicability of Prediction Model Studies.”** Methodological guideline. [DOI](https://doi.org/10.7326/M18-1376)
    Provides a structured risk-of-bias/applicability assessment. It can guide a limitations audit of sampling, outcome definition, and evaluation.

55. **Riley et al. (2020), “Calculating the sample size required for developing a clinical prediction model.”** Methods paper. [DOI](https://doi.org/10.1136/bmj.m441)
    Provides principled sample-size methods. It cautions against inferring evidence strength from convenience benchmark size alone.

56. **Shih et al. (2019), “Augmenting the National Institutes of Health Chest Radiograph Dataset with Expert Annotations of Possible Pneumonia.”** Dataset/annotation paper. [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC8017407/); [DOI](https://doi.org/10.1148/ryai.2019180041)
    Describes expert bounding-box annotation of pulmonary opacities that may represent pneumonia for the RSNA challenge, including multi-reader review/adjudication. It establishes RSNA's distinct annotation semantics and NIH lineage; the opacity task is not interchangeable with a ChestX-Det10 disease class.

57. **Dumbrique et al. (2024), “Pneumothorax detection and segmentation from chest X-ray radiographs using a patch-based fully convolutional encoder-decoder network.”** Primary study. [DOI/full text](https://doi.org/10.3389/fradi.2024.1424065)
    Proposes P-DeSeRay for pneumothorax detection and segmentation, evaluates on SIIM-ACR and a private hospital dataset, and reports an ablation in which mixed Tversky-plus-focal loss improves over Tversky alone. This is direct evidence that routine SIIM-only architecture/loss comparison is already crowded; any SIIM study would need a distinct question and recovered authorized data.

## Evidence synthesis and topic choice

### What the papers support

- Keep ChestX-Det10, RSNA, and SIIM targets, splits, and metrics separate.
- Report ChestX-Det10 native recall at its specified FP/image points and IoU
  0.5; RSNA mAP at IoU 0.4; and SIIM Dice only if valid source data are
  recovered. Never average them into one headline score.
- Audit image/patient provenance and possible duplication before any
  cross-dataset or external-validation claim. NIH lineage is a risk signal,
  not proof of overlap.
- Preserve whether supervision is report-derived, expert assigned,
  image-level, box-level, or mask-level. Do not treat attention maps as
  localization ground truth.
- Keep SIIM blocked until a complete authorized source is verified and image
  pairing, RLE order, dimensions, empty masks, and official Dice handling
  pass tests.
- Save the full pipeline specification: sources, splits, grouping, decoding,
  transformations, prediction serialization, evaluator, model settings, and
  seeds.

### What still needs evidence

1. Whether a blinded reread study is permissible and feasible, including
   radiologist availability, sampling, annotation instructions, adjudication,
   and a prespecified analysis of reader-to-reader variation.
2. Whether the closest reader-variability and localization studies already
   answer the proposed question; the current focused literature review does
   not prove novelty.
3. Whether the SIIM source can be recovered completely and lawfully; the
   local archive has not been validated as usable.
4. Whether image/patient/source identifiers support a valid split and
   duplicate audit; NIH lineage alone does not prove overlap.
5. Whether each dataset provides enough representative cases and
   task-specific annotations for informative confidence intervals and
   prespecified strata.

### Decision

The **overarching project topic** is proposed: how annotation type and
dataset shift affect localization learning and evaluation in chest
radiographs. The **lead all-three paper concept** is model localization
relative to independent reader variability; it is conditional on new blinded
rereads, SIIM recovery, and a completed novelty review. It is not yet
approved for implementation or claimed as novel.

The closest direct work establishes that SIIM pneumothorax localization,
RSNA opacity detection, and ChestX-Det10 detection already have prior art.
Routine model comparisons, a simple AP-versus-native-recall table, or
modular data-loader engineering alone are weak contributions. The next
research action is therefore to validate whether the reader-relative
question can be executed: confirm reader availability/permissions, establish
a reread sampling and adjudication protocol, recover/verify SIIM, and
complete targeted prior-art searches for reader disagreement, observer
variability, and localization evaluation. Run the overlap/provenance audit
before cross-dataset training or external-test claims.

If the reread study is infeasible, investigate pneumothorax box-to-mask
transfer as a two-dataset paper only after SIIM recovery and a separate
novelty check. Keep RSNA as an independent possible-opacity study. If neither
question survives feasibility and novelty checks, retain the work as a
high-quality reproducibility/engineering project rather than manufacturing
a novelty claim.

**Paper title: premature.** Name the paper only after the question,
comparator, reader protocol, dataset availability, and study protocol are
justified.

## Dataset requirements and roles

| Dataset | Native annotation/task | Current local status | Role in this project |
|---|---|---|---|
| [ChestX-Det10](../dataset_assessment.md#compact-paper-shortlist) | 2D boxes for 10 thoracic findings, including pneumothorax; supplied train/test split; recall at 0.05, 0.1, and 0.2 false positives per image, with IoU 0.5. | Train/test image archives and JSON annotations are locally present. Annotation structure and ZIP integrity have been checked, but image-to-box dimension checks, visual review, and patient/study split independence remain open. | **Candidate reader-study site and feasibility pilot.** Use its boxes and native metric; do not assume its released boxes expose independent per-reader annotations. |
| [RSNA Pneumonia Detection Challenge](../dataset_assessment.md#compact-paper-shortlist) | Detection of lung opacities considered possible pneumonia; DICOM images, multiple box rows for positive studies, and negative studies. The official challenge metric is mAP at IoU 0.4; public test labels are unavailable in the local bundle. | Training archive and annotations are locally present and structurally checked. Patient IDs are available for grouped internal train/validation splits. Verify current terms and reproduce the official evaluation protocol before any benchmark claim. | **Candidate reader-study site for a distinct opacity-box task.** Do not map its labels to ChestX-Det10 classes or present the unlabeled public test set as evaluated. Independent reader annotations and a reread protocol must be arranged. |
| [SIIM-ACR Pneumothorax Segmentation](../dataset_assessment.md#compact-paper-shortlist) | Pneumothorax segmentation masks encoded as RLE, not native box detection labels; the challenge uses a Dice-based score. A bounding box could be derived from a valid mask, but this changes the target protocol and needs explicit evaluation rules. | The local purported ZIP is unreadable and incomplete as verified. The official challenge notes that training images were hosted separately and may no longer be available. A complete, authorized, checksum-verified source has not been established. | **Blocked but central to the all-three proposal.** No reader-relative mask study or box-to-mask transfer is possible until a verified source is recovered. Preserve segmentation-native analysis if it becomes usable. |

“Three datasets are present in the inventory” does not mean “three datasets
are ready for one experiment.” At present, ChestX-Det10 and RSNA support
distinct box-detection tasks; SIIM-ACR is not usable locally and has a
different native target. The study must report these boundaries explicitly.
Because ChestX-Det10 and RSNA both describe NIH ChestX-ray data lineage,
deduplication/provenance checks across available image identifiers are a
required gate before using one as an external test for the other. This is a
risk to investigate, not a claim that the local subsets overlap.

## Candidate contribution and limits

Potential contributions to investigate—not claims to make yet:

1. A reader-relative analysis comparing model-to-reader localization with
   reader-to-reader disagreement, using blinded independent rereads and
   reporting each dataset/task separately. This is the lead all-three paper
   concept and depends on reader resources, permissions, SIIM recovery, and
   a completed novelty review.
2. If the all-three reader study is infeasible, a pneumothorax box-to-mask
   transfer analysis between ChestX-Det10 and SIIM, only if SIIM is recovered
   and the transfer hypothesis is supported by targeted prior-art review.
3. A separate RSNA possible-opacity localization study if a specific,
   consequential question is established; preserve its own target, patient
   grouping, and native metric.
4. A validated, reusable preparation/evaluation implementation recording
   provenance, split definition, evaluator version, and run configuration.
   Treat this as enabling infrastructure unless the study demonstrates a
   substantive methodological contribution.

Do **not** claim a universal detector, cross-hospital robustness, clinical
utility, or a shared multi-class task based on these resources alone. Similar
label names are not sufficient to establish equivalent target definitions.

## Minimum study design requirements

Before training for a paper result, freeze a short protocol containing:

- the study question, hypothesis, intended claim, and falsifiable outcome;
- the related-work search, inclusion/exclusion rules, and gap table;
- dataset versions, citations, license/terms review, source checksums, and
  readiness decision for each dataset;
- target definitions and any explicit cross-dataset ontology mapping;
- official split use and the independent grouping unit (patient/study where
  available); training-only validation procedure and held-out test policy;
- primary metric, operating point, evaluator implementation/version, and
  secondary metrics with complete definitions;
- baseline architecture, initialization, preprocessing/rendering, training
  config, seeds, checkpoint-selection rule, and planned ablations;
- per-class/per-size support and error analysis, uncertainty method, and
  resource constraints;
- privacy-safe artifact handling and a rule that raw data, derived images,
  identifiers, credentials, and checkpoints do not enter Git.

Preserve each dataset's native protocol. A metric conversion or target
conversion must be specified before inspecting final test results. Use
validation only for model, threshold, and checkpoint decisions. Report all
planned seeds and failed runs, not only the best run.

## Research and implementation gates

### Gate 1 — establish prior art and a defensible gap

Search primary papers, challenge reports, official dataset records, and
official evaluation code for ChestX-Det10, RSNA Pneumonia, SIIM-ACR, CXR
object detection/segmentation, low-FP/FROC and mAP evaluation, evaluator
reproducibility, image/patient leakage, data provenance, and external
validation. Search scholarly indexes and paper references/citations. Record
search date, exact query, source, task, datasets, split, metric,
contribution, limitations, and relation to the candidate question. Verify
that each cited work actually uses the dataset/task/metric stated; include
negative and conflicting findings, not only work that appears to support the
hypothesis.

**Pass condition:** a literature matrix shows a specific unanswered question,
not merely that a dataset or architecture has not been tried in this
repository. Explicitly check prior cross-dataset use of the same resources
and shared NIH source lineage. If no credible gap remains, keep the work as a
reproducible engineering baseline and do not frame it as a novel paper.

### Gate 2 — prove data and evaluation readiness

For ChestX-Det10, decode representative images, validate every referenced
image and box against dimensions, render overlays, inspect duplicates and
split/group overlap where IDs permit, and reproduce the native evaluator on
synthetic hand-checkable cases. For RSNA, verify DICOM rendering, aggregate
CSV rows per patient/image, preserve negatives, group by `patientId`, and
document the unlabeled public test boundary. Keep SIIM blocked until a
complete authorized source passes integrity and mask checks.

**Pass condition:** a reviewed preflight report, accepted data terms, tested
reader, and a reproducible evaluation protocol for every dataset used in the
study. For SIIM segmentation, verify RLE pixel order, image dimensions,
empty-mask handling, and the challenge Dice implementation against synthetic
cases and overlays before training.

### Gate 3 — freeze the question and protocol

Freeze one shared scientific hypothesis and state which datasets are
task-specific case studies versus separate follow-up studies. For an
all-three reader study, predefine the reread sample, within-dataset
comparators, native metrics, analysis, and acceptance criteria before model
experiments. Do not infer the final question from whichever metric/model
produces the most attractive result.

### Gate 4 — baseline, analysis, and reporting

Run the minimum documented baseline, then only the ablations required by the
question. Analyze errors and uncertainty at the appropriate image/patient
unit. Reserve held-out test evaluation for the prespecified final analysis.
State limitations and avoid claims beyond the sampling and annotation
protocol.

## Decision record

- **Is there a real overarching research topic?** Yes, proposed: how
  annotation type and dataset shift affect localization learning and
  evaluation in chest radiographs.
- **Is one paper question selected?** A lead hypothesis is identified:
  compare model-to-reader localization with reader-to-reader disagreement
  across task-appropriate annotations. It remains conditional, not an
  approved or novel claim.
- **Can one paper use all three datasets now?** No. SIIM-ACR is blocked
  locally; new blinded rereads and permission are not established; targets
  and native metrics differ. All three can be used only as separate
  task-specific case studies under a common reader-relative hypothesis.
- **What if that design is infeasible?** Consider a ChestX-Det10/SIIM
  pneumothorax box-to-mask transfer paper after SIIM recovery; retain RSNA
  for a separate opacity-localization study. Do not force RSNA into the
  pneumothorax paper.
- **Next action:** determine whether independent reader rereads are
  logistically and ethically feasible, resolve SIIM source availability,
  finish the closest-paper review, and audit overlap/provenance before
  freezing the paper protocol or starting targeted model training.

## Starting sources

- [ChestX-Det10 paper](https://arxiv.org/abs/2006.10550) and
  [authors' dataset/evaluation repository](https://github.com/Deepwise-AILab/ChestX-Det10-Dataset).
- [RSNA Pneumonia Detection Challenge](https://www.rsna.org/artificial-intelligence/ai-image-challenge/rsna-pneumonia-detection-challenge-2018),
  [Kaggle dataset](https://www.kaggle.com/competitions/rsna-pneumonia-detection-challenge/data),
  and [competition rules](https://www.kaggle.com/competitions/rsna-pneumonia-detection-challenge/rules).
- [SIIM-ACR Pneumothorax Segmentation data and instructions](https://www.kaggle.com/competitions/siim-acr-pneumothorax-segmentation/data).
- [Local dataset evidence and access assessment](../dataset_assessment.md).
- [Local task scope and candidate research questions](research_findings.md).
- [Detection workflow and evaluation safeguards](detection_workflow.md).
