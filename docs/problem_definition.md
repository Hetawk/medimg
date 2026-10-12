# Project Problem Definition

**Status:** Provisional research brief; not a novelty claim or a frozen
protocol.
**Last reviewed:** 2026-10-12
**Decision gate:** Complete the literature review and confirm data access and
readiness before selecting a paper question or training models.

## Working topic

**Evidence-first research on reliable localization in annotated chest
radiographs**

Our project topic is reliable, reproducible study of annotated chest
radiographs, with each dataset kept faithful to its native task. The leading
paper-topic candidate is to study whether specific data-preparation and
evaluation choices materially change localization conclusions on
ChestX-Det10, then test only a justified, separate replication on RSNA.

This is a working direction, not an approved paper question or novelty
claim. Existing papers already introduce these tasks, and ChestX-Det10
already reports both AP and its native low-FP recall measure. A paper cannot
claim novelty simply because this repository implements adapters, trains
another detector, or reports both scores.

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

## Provisional research question

> On ChestX-Det10, do well-defined differences in box matching, FROC
> interpolation, or threshold selection materially change reported native
> detection performance or scientific conclusions for identical frozen
> predictions?

This is a **candidate**, not an approved final question. Its scope must be
made testable by Gate 1: the published evaluator's implementation should be
compared against its documented protocol, not arbitrary alternative
definitions. Test the metric first using synthetic cases, then use identical
frozen predictions for paired evaluator comparisons. If exact evaluator
behavior matches the documented protocol and no meaningful ambiguity exists,
this question is not a paper contribution. Analyze any other task separately.
Do not average recall at fixed false-positive rates, box mAP, and Dice into a
common score.

ChestX-Det10 is the primary pilot because its native protocol is documented
and its local source files are structurally readable. RSNA is a possible
separate study only if the question can be meaningfully replicated under its
own mAP protocol, patient-grouped validation, and data terms. SIIM-ACR is
blocked and has a distinct segmentation target. If the proposed sensitivity
analysis is already well covered, or no controlled comparison is feasible,
narrow or replace the question before implementing training.

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
| Dumbrique et al. (2024), [P-DeSeRay](https://doi.org/10.3389/fradi.2024.1424065), and the [SIIM-ACR challenge](https://www.kaggle.com/competitions/siim-acr-pneumothorax-segmentation/data) | Proposes a patch-based fully convolutional encoder-decoder for pneumothorax detection/segmentation, evaluates on SIIM-ACR and a private hospital dataset, and reports benefit from a mixed Tversky/focal loss ablation. | Routine SIIM architecture/loss comparisons already have direct precedent. SIIM is a separate segmentation task and unusable from the current local archive. |

### Candidate-topic comparison

| Candidate topic | Proposed test | Feasibility | Main weakness / decision |
|---|---|---|---|
| **1. ChestX-Det10 measurement sensitivity** | Freeze identical predictions; compare the authors' evaluator with an independently tested implementation and report native FROC plus separately defined AP. Test whether scoring conventions change results or conclusions. | Highest: local archives/JSON are available, and evaluator tests can be built with synthetic predictions before training. | The dataset paper already reports both AP and fixed-FP recall. Proceed as a paper only if a consequential, previously unaddressed ambiguity exists; otherwise it is a correctness check, not a paper topic. |
| **2. ChestX-Det10 integrity/provenance audit** | Validate image coverage, decoded dimensions, box overlays, duplicates, split provenance, and recoverable patient/study separation; quantify model impact only if a consequential issue is found. | High as required engineering, but patient/study metadata may be missing. | A generic checklist is incremental. A paper depends on a material, independently verified finding or effect. |
| **3. RSNA DICOM-rendering sensitivity** | Compare prespecified, standards-consistent DICOM rendering policies using a fixed detector, patient-grouped validation, and mAP at IoU 0.4. | Moderate: labeled archive and `patientId` exist, but renderer, scorer, and terms need verification. | Plausible alternative if a deeper search establishes an under-studied, consequential question. Could be only engineering if choices are arbitrary or settled. Keep separate from ChestX-Det10. |
| **4. Cross-dataset transfer / NIH-lineage overlap** | First identify exact-image/patient matches and establish a genuinely shared target; only then consider transfer/external validation with a sensitivity analysis excluding matches. | Low to moderate: shared source lineage motivates an audit but does not prove overlap. | Do not select now. No common ontology is justified; do not call either set an independent external test without evidence. |
| **5. SIIM mask segmentation / mask-to-box** | Recover valid images/masks and reproduce Dice segmentation first. Prespecify any derived-box analysis as a separate target. | Not currently feasible; local archive is incomplete/unusable. | Exclude unless complete authorized data are recovered. |

**Project-level topic recommendation:** reliable, task-faithful evaluation of
annotated chest-radiograph datasets. Begin with the ChestX-Det10 integrity
and evaluator pilot; keep RSNA separate and SIIM blocked. Do **not** yet
approve a paper topic or novelty claim. The leading paper hypothesis is
evaluator/endpoint sensitivity only if the next focused literature search
finds an exact, unaddressed ambiguity; otherwise pivot rather than stretching
the claim.

The plausible added value is therefore not a new disease detector. The
candidate is a transparent audit of whether specific data and evaluation
decisions materially affect task-native conclusions. The current review does
not prove that this gap exists.

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

1. Whether ChestX-Det10 scorer details create any meaningful ambiguity
   beyond choices already disclosed in its paper and evaluator.
2. Whether controlled DICOM-rendering choices on RSNA have an
   under-investigated, consequential effect on its native box metric.
3. Whether patient/source identifiers support a valid split and overlap
   audit; NIH lineage alone does not prove duplicate images or patients.
4. Whether the SIIM source can be recovered completely and lawfully; the
   local archive has not been validated as usable in this review.
5. Whether any exact version of these candidate studies has already been
   published. A focused 57-publication bibliography is not exhaustive and
   does not prove novelty.

### Decision

The **project topic** is selected: reliable, task-faithful evaluation of
annotated chest radiographs. The **paper topic is not selected yet**. Begin
with ChestX-Det10 data-integrity checks and synthetic validation of its
official evaluator. In parallel, do a focused search for scorer-sensitivity
studies and RSNA DICOM-rendering studies. Promote one to the paper question
only if it is both under-addressed and experimentally testable with our
assets.

The closest direct paper review confirms that a normal detector comparison,
a simple AP-versus-native-recall table, or modular data-loader engineering
alone would be weak. If no consequential effect or research gap survives the
next review, keep the work as a high-quality reproducibility/engineering
project instead of forcing a novelty claim. Do not select SIIM as the
current topic while its source is unavailable.

**Paper title: premature.** Name the paper after the question, comparator,
and study protocol are justified—not before.

## Dataset requirements and roles

| Dataset | Native annotation/task | Current local status | Role in this project |
|---|---|---|---|
| [ChestX-Det10](../dataset_assessment.md#compact-paper-shortlist) | 2D boxes for 10 thoracic findings, including pneumothorax; supplied train/test split; recall at 0.05, 0.1, and 0.2 false positives per image, with IoU 0.5. | Train/test image archives and JSON annotations are locally present. Annotation structure and ZIP integrity have been checked, but image-to-box dimension checks, visual review, and patient/study split independence remain open. | **Primary feasibility pilot.** Preserve the native metric. Only pursue a metric-sensitivity paper if a meaningful gap survives the targeted literature review. |
| [RSNA Pneumonia Detection Challenge](../dataset_assessment.md#compact-paper-shortlist) | Detection of lung opacities considered possible pneumonia; DICOM images, multiple box rows for positive studies, and negative studies. The official challenge metric is mAP at IoU 0.4; public test labels are unavailable in the local bundle. | Training archive and annotations are locally present and structurally checked. Patient IDs are available for grouped internal train/validation splits. Verify current terms and reproduce the official evaluation protocol before any benchmark claim. | **Separate pneumonia experiment or replication.** Never merge its opacity targets with ChestX-Det10 disease classes or present its unlabeled public test set as an evaluated test set. Include only if the reviewed question and available labels support it. |
| [SIIM-ACR Pneumothorax Segmentation](../dataset_assessment.md#compact-paper-shortlist) | Pneumothorax segmentation masks encoded as RLE, not native box detection labels; the challenge uses a Dice-based score. A bounding box could be derived from a valid mask, but this changes the target protocol and needs explicit evaluation rules. | The local purported ZIP is unreadable and incomplete as verified. The official challenge notes that training images were hosted separately and may no longer be available. A complete, authorized, checksum-verified source has not been established. | **Blocked; not currently an experiment dataset.** Record as a candidate extension only. Do not download from or redistribute an unverified mirror, and do not count it as the third usable dataset. If access is resolved, keep segmentation native and treat any mask-to-box conversion as a separate prespecified analysis. |

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

1. A reproducible, paired audit of specific ChestX-Det10 matching,
   interpolation, or threshold-selection details, **only if** prior work
   leaves an ambiguity and it changes reported conclusions.
2. A prespecified RSNA DICOM-rendering study if an exact rendering question
   is both under-studied and consequential; use a separate task-specific
   experiment and patient grouping.
3. A validated, reusable preparation/evaluation implementation that records
   data provenance, split definition, evaluator version, and run config.
   Treat this as enabling infrastructure unless the literature review shows
   a substantive methodological contribution.
4. If SIIM access is resolved, add a separate native segmentation baseline.
   If a detection experiment is also scientifically justified, analyze
   mask-to-box conversion separately and avoid describing derived boxes as
   radiologist-annotated boxes.

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

Choose one primary dataset/question and decide whether another dataset is a
separate replication or out of scope. Write the comparator and acceptance
criteria before model experiments. Do not infer the final question from
whichever metric/model produces the most attractive result.

### Gate 4 — baseline, analysis, and reporting

Run the minimum documented baseline, then only the ablations required by the
question. Analyze errors and uncertainty at the appropriate image/patient
unit. Reserve held-out test evaluation for the prespecified final analysis.
State limitations and avoid claims beyond the sampling and annotation
protocol.

## Decision record

- **Problem defined at the project level?** Yes: reliable, task-aware
  preparation and evaluation of annotated CXR datasets.
- **A paper problem and novelty claim established?** **Not yet.** The project
  topic is selected; a paper-level hypothesis awaits targeted prior-art
  review and data-readiness gates.
- **Are all three local datasets ready for a unified experiment?** No.
  ChestX-Det10 is the primary pilot, RSNA is a separate task, and SIIM-ACR is
  blocked and segmentation-native.
- **Next action:** verify the exact ChestX-Det10 evaluator behavior with
  synthetic cases and complete image/box preflight; search targeted
  evaluator-sensitivity and RSNA DICOM-rendering literature before choosing
  a paper hypothesis or adding training functionality.

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
