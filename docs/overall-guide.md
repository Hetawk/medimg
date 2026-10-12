You're right. The previous response was still too broad and did not go deep enough into the individual machine learning tasks. You are asking for something much more comprehensive: a large, detailed, technically rigorous reference covering the major machine learning problem types, model architectures, training strategies, evaluation metrics, robustness techniques, and deployment practices across the field.

For example, computer vision alone includes image classification, object detection, semantic segmentation, instance segmentation, panoptic segmentation, keypoint detection, pose estimation, object tracking, optical flow, depth estimation, image registration, image restoration, and image generation. Each has different training requirements, failure modes, and evaluation criteria.

The same applies to NLP, time-series modeling, recommendation systems, graph learning, generative AI, reinforcement learning, scientific machine learning, and many other fields.

Let's structure this as a comprehensive Machine Learning Best Practices Handbook, with shared engineering standards and detailed playbooks for individual tasks.

# Comprehensive Machine Learning Best Practices Handbook

## Part 1. Universal engineering standards

These principles form the foundation for every task-specific playbook.

### 1. Problem definition and experimental design

Before choosing a model, establish:

- Problem formulation: What is being predicted, generated, ranked, estimated, discovered, or controlled?
- Learning paradigm: Supervised, unsupervised, self-supervised, semi-supervised, reinforcement, online, or hybrid learning.
- Inputs and outputs: Data modalities, dimensions, output format, and prediction constraints.
- Deployment environment: Offline batch processing, real-time inference, edge devices, cloud services, or embedded systems.
- Primary objective: The metric or practical outcome that determines whether the model is useful.
- Acceptance criteria: Minimum performance, maximum latency, acceptable failure rate, memory limits, and relevant safety constraints.
- Baseline: A simple, reproducible reference against which improvements can be measured.

Do not begin with an assumption that the largest neural network will be the best model. Model choice should follow the problem requirements and available evidence.

### 2. Data engineering and integrity

A robust data pipeline should include:

1. Data provenance and permission verification.
2. Schema validation and input-type checks.
3. Duplicate and near-duplicate detection.
4. Missing-data and corrupted-sample analysis.
5. Label quality and annotation consistency checks.
6. Outlier and distribution analysis.
7. Dataset versioning and reproducible splits.
8. Training–deployment distribution comparison.
9. Leakage prevention at both feature and sample levels.
10. Privacy, security, retention, and access controls.

The split must reflect the true unit of generalization. Images from the same patient, frames from the same video, samples from the same experiment, or transactions from the same entity may need to stay within one partition.

### 3. Model development and optimization

Every serious project should establish:

- A baseline model.
- A justified architecture and loss function.
- A documented preprocessing pipeline.
- A reproducible training configuration.
- A validation-based selection procedure.
- Appropriate regularization and augmentation.
- Hyperparameter optimization.
- Error analysis and ablation experiments.
- Independent final evaluation.
- Model and dataset versioning.

### 4. Evaluation and robustness

Evaluate not only average predictive performance, but also:

- Generalization to independent data.
- Sensitivity to realistic distribution shifts.
- Subgroup and rare-case performance.
- Confidence calibration and uncertainty where appropriate.
- Statistical variability across splits or seeds.
- Runtime, memory, and computational cost.
- Failure severity and recovery behavior.
- Production monitoring requirements.

These standards apply across the handbook, but the specific techniques and metrics must change with the task.

# Part 2. Computer vision: detailed task-by-task best practices

Computer vision deserves its own major section because different vision tasks solve fundamentally different problems. A classification model, detector, segmenter, tracker, and image generator should not share one generic evaluation procedure.

## 2.1 Image classification

[What Is Computer vision and Why Does It Matter? | NVIDIA Glossary](https://images.openai.com/static-rsc-4/gxv9OiSjqDQHp9sEjeVJj7kjDAHbxUL-dYkscDAd5CHE2-SrW8aq-7TA7EdRn7WRHXnqK_etIkpSuHXxH076r6iCz-8ximdIqOt2f5b585YgTjJ2dfe3AgXURo3qOzP0e6z3rYfgiHO3mPd1CrF-PsZyHT1VQ3t_l6G58pq0tRw?purpose=inline)

Objective: Assign one or more labels to an image.

Examples: animal recognition, defect classification, medical-image diagnosis, plant disease recognition, scene classification.

Common model families

- CNNs: ResNet, ConvNeXt, EfficientNet.
- Vision transformers: ViT, Swin Transformer.
- Self-supervised or pretrained visual encoders.
- Multimodal vision-language encoders for suitable zero-shot or transfer-learning tasks.

Best practices

1. Determine whether the task is single-label, multilabel, hierarchical, or ordinal.
2. Inspect image dimensions, channels, color profiles, duplicates, and label quality.
3. Choose augmentation that preserves the label.
4. Use pretrained models when the dataset is limited and transfer learning is appropriate.
5. Compare against a simple baseline and a suitable pretrained baseline.
6. Monitor class-wise errors and the training–validation performance gap.
7. Calibrate probabilities if they will inform decisions.
8. Test external images, acquisition conditions, and relevant subgroups.

Evaluation metrics

- Top-1 and top-k accuracy.
- Macro-F1 and per-class precision/recall.
- ROC-AUC or PR-AUC where applicable.
- Log loss and calibration metrics.
- Confusion matrices and confidence intervals.

Common failures: label leakage, background shortcuts, severe class imbalance, duplicate images across splits, and poor performance on unseen acquisition conditions.

## 2.2 Object detection

[计算机视觉和机器视觉有什么区别？](https://images.openai.com/static-rsc-4/daqrDuMF5th-F0ZJZ9hjYEofIcVpt_LG7fs3wSn1jf_YkALMBFnv5h23oWBWYSWB--NupImv8i4J3yEQHDfSEczqz1texuHG0gB03Zzucg6lqvFCFsu7nvQemuUrq04xbXI1hNj9ELqYQZZVCy4EaglfSt7FZmdYRemo3NbWkX0?purpose=inline)

Objective: Identify objects, their classes, and their locations, typically using bounding boxes.

Examples: autonomous driving, pedestrian detection, industrial inspection, wildlife monitoring, medical-lesion detection.

Common model families

- Two-stage detectors: Faster R-CNN.
- One-stage detectors: RetinaNet and YOLO-family detectors.
- Transformer-based detectors: DETR and its variants.
- Specialized small-object or domain-specific detectors.

Best practices

1. Standardize annotation conventions, coordinate systems, box boundaries, and class definitions.
2. Audit missing objects, inaccurate boxes, and inconsistent annotations.
3. Analyze object sizes, aspect ratios, density, and occlusion.
4. Ensure geometric augmentations transform bounding boxes correctly.
5. Tune input resolution, feature-pyramid configuration, and object-scale handling.
6. Evaluate crowded scenes, small objects, partial visibility, and rare classes separately.
7. Tune confidence thresholds and non-maximum suppression using validation data.
8. Measure end-to-end inference speed, not only model forward-pass time.

Evaluation metrics

- Mean average precision (mAP).
- Average precision at specified intersection-over-union (IoU) thresholds.
- Recall at a specified number of detections.
- Per-class AP and AP by object size.
- False positives per image or per operating interval.
- Latency and throughput.

Common failures: missed small objects, duplicate detections, poor localization, false positives on background patterns, and inaccurate labels.

A detector can achieve good classification confidence while placing a box poorly. Therefore, localization quality and detection confidence must both be evaluated.

## 2.3 Semantic segmentation

[Perception](https://images.openai.com/static-rsc-4/GdkHg8kCscCb_32oAxmh5nHuub9uCDWT0An806E0pMQPiScgTU5W9CKVFX-uE-8FHdOyUhGAZM1Rh0ONhg5rDKDMWmD6JC872VO7Nrh9X5AeFrouL7I3bUMV8Bq21rwJWq0FerqQqplx40ZR4Cj-WUBPLOhvZXfGCzfRmlsdckQ?purpose=inline)

Objective: Assign a class to every pixel in an image.

Examples: road segmentation, organ segmentation, land-cover mapping, tumor-region analysis, material classification.

Common model families

- U-Net and U-Net variants.
- DeepLab.
- Feature-pyramid and encoder–decoder networks.
- SegFormer and other transformer-based segmenters.
- Foundation-model-assisted segmentation pipelines, where appropriate.

Best practices

1. Validate image–mask alignment, image orientation, mask encoding, and class IDs.
2. Ensure resizing and geometric transformations preserve correct mask geometry and use suitable interpolation for categorical masks.
3. Address rare classes and severe pixel imbalance without letting background dominate the objective.
4. Select loss functions based on the task: cross-entropy, Dice loss, focal loss, or carefully justified combinations.
5. Evaluate both region overlap and boundary accuracy.
6. Inspect thin structures, tiny objects, ambiguous boundaries, and disconnected regions.
7. Compare full-resolution and tiled inference where images are large.
8. Check consistency across resolutions, devices, and image acquisition conditions.

Evaluation metrics

- Mean IoU and per-class IoU.
- Dice coefficient.
- Pixel-level precision and recall.
- Boundary F-score or boundary IoU.
- Hausdorff distance for suitable boundary-sensitive applications.
- Inference latency and peak memory.

Common failures: misaligned masks, incorrect interpolation, disappearing thin structures, poor boundaries, class collapse, and high aggregate scores that conceal failure on small but important regions.

### Choosing between Dice and IoU

For a binary predicted region and ground-truth region:

\\[ \operatorname{Dice}=\frac{2|P\cap G|}{|P|+|G|} \\]

\\[ \operatorname{IoU}=\frac{|P\cap G|}{|P\cup G|} \\]

They are closely related but not identical. Neither alone captures all boundary errors, object-count errors, or clinical significance.

## 2.4 Instance segmentation

[From Thresholding to Generative Magic: A Deep Dive into Image Segmentation | by Himani | Feb, 2026 | Medium](https://images.openai.com/static-rsc-4/moxx8cBchYBosG3f-PmA5qpfmOK7KEP2MIhodZh697PPs_VUo4Imp2Cwluggu9d39WXmP_GL924K5SJiHooM9S3W0xMPgzelwN4gL_dz-dWrxjLE5m3dZh9psnheQyesHRGsGHD4UGQ5VSf_PviRkO11ge0iQEJcmdX_GVS1_Yg?purpose=inline)

Objective: Produce a separate pixel mask for each individual object instance.

Examples: cell counting, individual fruit detection, microscopy, manufacturing inspection, robotic manipulation.

Common model families: Mask R-CNN, CondInst, SOLO-style models, and instance-segmentation variants of modern detectors.

Best practices

- Ensure every object instance has a consistent identity and mask.
- Evaluate touching or overlapping objects carefully.
- Include small, crowded, and partially occluded instances in validation.
- Avoid treating all pixels of the same class as one instance.
- Measure both detection and mask quality.
- Investigate missed instances, merged objects, and fragmented masks.
- For cell or particle counting, assess counting error separately from mask overlap.

Metrics: mask AP, box AP, AP by object size, precision/recall, instance-count error, and boundary metrics where relevant.

Key distinction: semantic segmentation can label a group of same-class objects as one continuous region; instance segmentation must distinguish individual objects.

## 2.5 Panoptic segmentation

Objective: Combine semantic and instance segmentation into a unified scene representation.

The model identifies stuff regions, such as road, sky, or grass, and individual thing instances, such as cars, people, or animals.

Best practices

- Maintain consistent class taxonomies across semantic and instance labels.
- Define how overlapping predictions and void regions are handled.
- Evaluate both thing and stuff categories.
- Check instance separation, region completeness, and small-object performance.
- Audit errors caused by conflicts between the semantic and instance branches.

Metrics: Panoptic Quality (PQ), Segmentation Quality (SQ), Recognition Quality (RQ), and relevant per-class results.

PQ combines segmentation quality with recognition quality; a single overall score should not replace inspection of the two components.

## 2.6 Keypoint detection and landmark localization

[A Comprehensive Understanding of Human Pose Estimation | by Amithesh Gupta | Medium](https://images.openai.com/static-rsc-4/2tsamH9NXeCdwgEj2zJE2NKXm_nPp0aiflJdIII9Ae0OtD8djd1gDMsLk1MHJ59kiKiN63iQQAbhtti27ZbwEhvSFKm1gvaZMcFfMoo3UVappPUl2Q7qGDIrvestbNWj6tvk3v1cZmWzGwE5c8QQh3RfhBrkNtA6dyufG2M3QJk?purpose=inline)

Objective: Predict the coordinates of meaningful points.

Examples: human joints, facial landmarks, anatomical landmarks, industrial alignment points.

Best practices

- Define coordinate conventions and visibility labels consistently.
- Preserve coordinate transformations through resizing, cropping, and augmentation.
- Handle occluded and out-of-frame landmarks explicitly.
- Evaluate performance by landmark, scale, and visibility.
- Distinguish detection failure from localization error.
- Quantify annotation uncertainty for inherently ambiguous landmarks.

Metrics: mean keypoint error, normalized mean error, PCK, OKS-based AP for human pose, and task-specific localization tolerances.

For medical landmarks, report errors in physical units such as millimeters when reliable image-spacing information is available.

## 2.7 Human pose estimation

Pose estimation predicts a structured arrangement of joints or body landmarks, often across multiple people.

Model approaches

- Heatmap-based keypoint models.
- Direct coordinate regression.
- Top-down pipelines that detect people before estimating pose.
- Bottom-up pipelines that detect joints and group them.
- Temporal models for video-based pose estimation.

Best practices

1. Evaluate crowded scenes and unusual poses.
2. Separate person-detection failures from joint-localization failures.
3. Check left/right joint consistency and anatomical plausibility.
4. Test occlusion, motion blur, camera-angle changes, and unusual body proportions.
5. For video, evaluate temporal stability as well as per-frame accuracy.
6. Avoid assuming that visually plausible predictions are anatomically correct.

Metrics: PCK, OKS-based AP, joint-wise error, pose-level recall, and temporal jitter where applicable.

## 2.8 Multi-object tracking

Objective: Detect objects over time and maintain consistent identities across video frames.

Applications include traffic analysis, sports analytics, surveillance, warehouse robotics, and cell tracking.

Best practices

- Evaluate detection quality and association quality separately.
- Test occlusions, objects leaving and re-entering the scene, and similar-looking objects.
- Use sequence-level data splits to avoid video leakage.
- Evaluate identity switches, fragmentation, and track continuity.
- Measure the effect of detector errors on downstream tracking.
- Check latency and behavior under variable frame rates.

Metrics: HOTA, IDF1, MOTA, identity switches, track fragmentation, and tracking latency.

A tracker may have reasonable frame-level detections but still fail badly when identities change. This is why detection AP alone is insufficient.

## 2.9 Single-object tracking

Objective: Follow a particular target through successive frames, often given its initial location.

Best practices

- Test appearance changes, occlusion, rapid movement, scale changes, and distractor objects.
- Evaluate long sequences rather than isolated frames.
- Use consistent initialization and benchmark protocols.
- Separate failure to locate the target from poor box precision.
- Test re-detection and recovery after temporary disappearance.

Metrics: success plots, area under the success curve, precision, normalized precision, and robustness or failure counts depending on the benchmark.

## 2.10 Optical flow and motion estimation

Objective: Estimate pixel-level displacement between frames.

Best practices

- Validate the coordinate convention and direction of flow vectors.
- Include fast motion, occlusions, textureless regions, and motion boundaries.
- Test sensitivity to image resolution and frame intervals.
- Evaluate motion boundaries separately from smooth regions.
- Avoid relying exclusively on synthetic benchmark data when real-world deployment differs substantially.

Metrics: endpoint error, percentage of erroneous flow estimates, and motion-boundary accuracy.

## 2.11 Depth estimation and 3D vision

These tasks estimate scene geometry, depth maps, 3D object positions, point clouds, or scene structure.

Best practices

- Distinguish metric depth from relative depth.
- Validate camera intrinsics, extrinsics, and calibration.
- Handle invalid depth measurements and sensor-specific artifacts.
- Test reflective, transparent, dark, distant, and textureless surfaces.
- Evaluate scale consistency across scenes.
- Check coordinate frames and units throughout the pipeline.

Metrics: absolute relative error, squared relative error, RMSE, threshold accuracy for depth; 3D IoU, translation/rotation error, and point-cloud distances for appropriate 3D tasks.

## 2.12 Image restoration and enhancement

Includes denoising, deblurring, super-resolution, compression artifact removal, and low-light enhancement.

Best practices

- Define the degradation model and ensure test degradations resemble deployment conditions.
- Prevent near-duplicate or source-image leakage.
- Evaluate both perceptual quality and fidelity to the reference.
- Inspect hallucinated details, ringing artifacts, texture loss, and edge distortions.
- Evaluate on real degraded images in addition to synthetic corruptions.
- In medical imaging, assess whether enhancement changes diagnostically meaningful features.

Metrics: PSNR, SSIM, LPIPS, perceptual or expert evaluation, and task-specific downstream accuracy.

A visually sharper image is not necessarily a more faithful image. Generative restoration models may invent plausible details that were not present in the source.

## 2.13 Image registration

Objective: Align images from different times, viewpoints, modalities, or coordinate systems.

Applications include medical-image registration, satellite imagery, microscopy, and panorama construction.

Best practices

- Validate coordinate conventions and transformation composition.
- Evaluate alignment in clinically or operationally important regions.
- Test large deformations, modality changes, and low-texture areas.
- Distinguish image similarity from actual anatomical or geometric correspondence.
- Evaluate inverse consistency and transformation plausibility where applicable.

Metrics: landmark target-registration error, Dice after alignment, image similarity, and deformation regularity.

## 2.14 Image generation and image-to-image translation

Includes text-to-image synthesis, inpainting, image editing, domain translation, and conditional image generation.

Best practices

- Separate image fidelity, diversity, and conditioning adherence.
- Evaluate memorization and training-data contamination.
- Test difficult prompts, rare concepts, and composition constraints.
- Check for artifacts, unsafe outputs, and demographic or domain biases.
- Use human evaluation when automated metrics do not reflect the intended output quality.
- For image-to-image tasks, measure whether required source information is preserved.

Metrics: FID, precision/recall for generated distributions, CLIP-based measures where appropriate, perceptual similarity, task-specific fidelity, and human preference evaluation.

## 2.15 Video understanding and action recognition

Includes action classification, temporal localization, event detection, video summarization, and video question answering.

Best practices

- Split by source video, subject, or recording session as appropriate.
- Preserve temporal ordering and sample frames consistently.
- Test long-duration context, camera changes, motion blur, and frame-rate variation.
- Evaluate event localization, not just video-level labels, when timestamps matter.
- Avoid leakage from near-identical frames.
- Assess temporal consistency and real-time processing constraints.

Metrics: video-level accuracy or mAP, temporal localization mAP, event-level recall, and latency.

## 2.16 Remote sensing and geospatial imagery

Includes land-cover classification, building extraction, road segmentation, object detection, change detection, and crop monitoring.

Best practices

- Split by geographic region or acquisition scene when spatial generalization matters.
- Account for spatial autocorrelation and overlapping image tiles.
- Normalize carefully across sensors and acquisition conditions.
- Test seasonal, geographic, resolution, and sensor shifts.
- Check georeferencing and coordinate-system correctness.
- Evaluate rare geographic classes separately.

Metrics: IoU, F1, mAP, change-detection precision/recall, and geospatial boundary or area error.

## 2.17 OCR and document vision

Includes text detection, text recognition, document layout analysis, table extraction, and handwriting recognition.

Best practices

- Evaluate detection, recognition, layout, and information extraction separately.
- Test scan quality, skew, low resolution, handwriting, and unusual fonts.
- Preserve reading order and table relationships.
- Normalize text consistently without erasing meaningful distinctions.
- Test complete-document accuracy, not only cropped text accuracy.

Metrics: character error rate, word error rate, text-detection AP, field-level exact match, and table-structure accuracy.

# Part 3. Natural language processing and language models

NLP tasks vary considerably: some require assigning labels to text, others extracting structured information, retrieving documents, generating answers, translating languages, or reasoning over long contexts.

## 3.1 Text classification

Examples include sentiment analysis, topic classification, spam detection, intent recognition, and document routing.

Approaches: TF-IDF with linear models, gradient-boosted models over text features, pretrained transformer encoders, and fine-tuned language models.

Best practices

- Split by document, author, conversation, or source when related text could otherwise leak across partitions.
- Normalize text only as much as the task permits.
- Test spelling errors, abbreviations, multilingual content, and domain-specific vocabulary.
- Inspect class-wise performance and ambiguous labels.
- Compare pretrained models against simpler baselines.
- Evaluate calibration if scores drive automated decisions.

Metrics: macro-F1, per-class precision/recall, accuracy, PR-AUC where appropriate, and calibration.

## 3.2 Named-entity recognition and information extraction

Examples: extracting names, organizations, dates, diagnoses, medications, contract terms, and invoice fields.

Best practices

- Define exact entity boundaries and annotation conventions.
- Handle nested, overlapping, and discontinuous entities if the task requires them.
- Evaluate entity-level matches, not merely token-level accuracy.
- Test unfamiliar entity names, rare categories, and domain-specific language.
- Check whether extraction errors alter the meaning of downstream records.
- Use constrained output schemas and validation when generating structured data.

Metrics: entity-level precision, recall, F1, exact-match accuracy for structured fields, and end-to-end extraction accuracy.

## 3.3 Machine translation

Best practices

- Evaluate language pairs and directions independently.
- Use test sets representative of the target domain.
- Inspect terminology, named entities, negation, numbers, and grammatical agreement.
- Include low-resource languages and code-switching where relevant.
- Assess both semantic preservation and fluency.
- Use qualified human evaluation for high-stakes or specialized translation.

Metrics: COMET, BLEU, chrF, and human adequacy/fluency assessment, chosen according to the task and evaluation protocol.

## 3.4 Summarization

Includes extractive summarization, abstractive summarization, meeting summaries, and long-document synthesis.

Best practices

- Establish whether factual coverage, brevity, completeness, or action-item extraction is most important.
- Compare generated statements with the source documents.
- Test long inputs, conflicting evidence, and missing context.
- Evaluate omissions, unsupported claims, attribution, and numerical accuracy.
- Assess whether the model preserves uncertainty and qualifications.
- Measure performance on realistic documents, not only short benchmark examples.

Metrics: ROUGE, BERTScore, factual-consistency measures, human judgments, and task-specific coverage and error rates.

Lexical similarity alone cannot establish factual correctness.

## 3.5 Question answering and retrieval-augmented generation

Separate the retrieval problem from the answer-generation problem.

Retrieval best practices

- Evaluate chunking, indexing, embedding choice, metadata filtering, and reranking.
- Include difficult negative examples and queries with no answer in the corpus.
- Test stale, duplicated, contradictory, and access-restricted documents.
- Evaluate retrieval recall at multiple values of \\(k\\).

Generation best practices

- Verify factual claims against retrieved evidence.
- Evaluate citation correctness and answer completeness.
- Test abstention when evidence is insufficient.
- Protect against prompt injection embedded in retrieved documents.
- Check access control throughout retrieval and generation.
- Test the entire pipeline rather than only the language model.

Metrics: Recall\@k, MRR, NDCG, answer correctness, groundedness, citation precision, abstention quality, and end-to-end task success.

## 3.6 Search and learning to rank

Examples: web search, product ranking, document retrieval, and candidate selection.

Best practices

- Define the relevance judgment protocol.
- Prevent user, query, and temporal leakage.
- Reconstruct realistic candidate sets.
- Account for position bias and exposure bias when using interaction data.
- Evaluate cold-start users and items.
- Measure latency and the quality of the complete retrieval-and-ranking pipeline.

Metrics: NDCG\@k, MAP, MRR, Recall\@k, precision at \\(k\\), and carefully designed online outcome measures.

## 3.7 Language-model fine-tuning

Includes supervised fine-tuning, instruction tuning, parameter-efficient tuning, preference optimization, and domain adaptation.

Best practices

1. Establish a base-model baseline before fine-tuning.
2. Remove sensitive data and evaluate dataset provenance.
3. Deduplicate against validation sets and known evaluation benchmarks.
4. Use training formats consistent with inference.
5. Tune learning rate, sequence length, batch size, and training duration carefully.
6. Evaluate catastrophic forgetting and regressions on general capabilities.
7. Test instruction adherence, factuality, safety, and domain-specific performance.
8. Compare full fine-tuning with parameter-efficient approaches such as LoRA when suitable.
9. Test deployment quantization and serving configurations separately from the original model.

Metrics: task-specific accuracy, exact match, human preference, instruction adherence, regression benchmarks, latency, and memory consumption.

## 3.8 Speech recognition and audio understanding

Includes automatic speech recognition, speaker identification, speech emotion analysis, sound classification, and audio event detection.

Best practices

- Split by speaker, session, or recording source where needed.
- Evaluate accents, background noise, microphone types, speaking rates, and overlapping speech.
- Preserve timestamps and speaker attribution where required.
- Distinguish transcription errors from punctuation and formatting errors.
- Test privacy and biometric-data handling for speaker-related systems.

Metrics: word error rate, character error rate, diarization error rate, event-level F1, and latency.

## 3.9 Text-to-speech and speech generation

Best practices

- Evaluate intelligibility, naturalness, pronunciation, and speaker consistency separately.
- Test unusual names, numbers, code-switching, and long-form synthesis.
- Measure latency and streaming behavior.
- Assess voice identity consistency and unauthorized voice imitation risks.
- Check artifacts, prosody, and output stability across repeated runs.

Metrics: intelligibility measures, MOS-based human evaluation, speaker similarity where relevant, latency, and task-specific pronunciation error.

## 3.10 Multimodal AI

Combines text, images, audio, video, structured data, or other modalities.

Best practices

- Align examples and timestamps correctly across modalities.
- Evaluate each modality independently and in combination.
- Test missing, corrupted, contradictory, or misleading modalities.
- Prevent source-level leakage between training and evaluation.
- Measure whether each modality adds value over unimodal baselines.
- Investigate modality dominance and shortcut learning.

Metrics: task-specific performance, cross-modal retrieval metrics, alignment accuracy, robustness to missing modalities, and modality-ablation results.

# Part 4. Tabular data, forecasting, and statistical learning

## 4.1 Tabular prediction

Tabular problems include classification, regression, risk prediction, ranking, and structured decision support.

Model families: linear and generalized linear models, Random Forests, gradient-boosted trees, support vector machines, and neural networks.

Best practices

- Validate feature definitions and prediction-time availability.
- Use training-only imputation, scaling, encoding, and feature selection.
- Treat categorical variables appropriately.
- Investigate missingness mechanisms and outliers.
- Test temporal and group-based splits when deployment requires future or unseen-entity predictions.
- Compare linear models and tree ensembles before adopting complex deep-learning models.
- Inspect calibration, subgroup errors, and feature dependence.
- Avoid interpreting feature importance as causal evidence.

Metrics: task-specific predictive metrics, calibration, subgroup performance, and decision utility.

## 4.2 Time-series forecasting

Forecasting requires special care because temporal leakage can make results look much better than they really are.

Best practices

- Establish naive, seasonal-naive, and simple statistical baselines.
- Use chronological validation and rolling-origin backtesting.
- Construct lags and rolling statistics using only information available at prediction time.
- Evaluate each forecast horizon separately.
- Model seasonality, trend, structural breaks, and changing variance where appropriate.
- Include exogenous features only if they will be available at forecast time.
- Evaluate prediction intervals when uncertainty affects decisions.
- Test across multiple forecast origins and changing operating conditions.

Metrics: MAE, RMSE, MASE, weighted error measures where appropriate, pinball loss, and interval coverage.

MAPE can be misleading when actual values are zero or close to zero.

## 4.3 Probabilistic prediction and uncertainty estimation

The goal is not merely to predict an outcome, but also to characterize uncertainty.

Best practices

- Distinguish aleatoric uncertainty from epistemic uncertainty where the modeling framework permits it.
- Test calibration on independent data.
- Evaluate performance under distribution shift.
- Verify prediction interval coverage and width.
- Use ensembles, Bayesian approaches, conformal prediction, or other suitable methods when justified.
- Avoid interpreting model confidence as a guarantee of correctness.

Metrics: negative log-likelihood, Brier score, CRPS, calibration error, interval coverage, and interval width.

## 4.4 Survival analysis

Used for time until death, failure, relapse, churn, or another event.

Best practices

- Represent right-censoring and other censoring mechanisms correctly.
- Prevent future information from entering predictors.
- Assess proportional-hazards assumptions when using Cox models.
- Evaluate predictions at clinically or operationally meaningful time horizons.
- Check calibration and performance across subgroups.
- Distinguish event-time prediction from binary classification at a fixed time.

Metrics: concordance index, time-dependent AUC, Brier score, integrated Brier score, and calibration at specific horizons.

## 4.5 Causal inference and treatment-effect estimation

Causal inference is different from ordinary predictive modeling: accurate prediction does not prove that a feature causes an outcome.

Best practices

- Define the causal question and estimand before modeling.
- Specify the assumptions needed for causal identification.
- Use causal diagrams and domain knowledge to reason about confounders.
- Choose methods appropriate to randomized or observational data.
- Avoid conditioning on inappropriate post-treatment variables.
- Conduct sensitivity analyses for unmeasured confounding.
- Validate against randomized evidence or known effects where feasible.

Evaluation: bias and coverage in simulations, sensitivity to assumptions, balance diagnostics, and agreement with credible causal evidence. Ordinary predictive accuracy is not sufficient.

# Part 5. Recommendation systems, anomaly detection, and specialized learning

## 5.1 Recommendation systems

Recommendation systems predict relevance or help users discover items, products, content, services, or connections.

Common approaches

- Popularity and rule-based baselines.
- Collaborative filtering.
- Matrix factorization.
- Content-based recommendation.
- Two-tower retrieval models.
- Learning-to-rank models.
- Sequential recommendation and session-based models.
- Hybrid and graph-based recommendation.

Best practices

1. Split interaction data chronologically when the goal is to predict future behavior.
2. Prevent future interactions from leaking into user or item features.
3. Evaluate cold-start users and items separately.
4. Account for exposure bias: an unclicked item may never have been shown.
5. Compare retrieval and ranking stages separately.
6. Evaluate diversity, novelty, coverage, and relevance rather than relevance alone.
7. Consider popularity bias and feedback loops.
8. Use online experiments carefully, with predefined outcome measures and guardrails.
9. Respect privacy and consent requirements for user behavioral data.

Metrics: Recall\@k, NDCG\@k, MAP, MRR, coverage, diversity, novelty, calibration, and appropriate online measures such as conversion or engagement.

## 5.2 Anomaly detection and outlier detection

These systems identify observations that differ from expected behavior.

Approaches: Isolation Forest, Local Outlier Factor, One-Class SVM, autoencoders, density estimation, and specialized temporal anomaly detectors.

Best practices

- Define what constitutes an anomaly operationally.
- Distinguish outliers from valid rare events.
- Avoid fitting thresholds on the final test set.
- Evaluate detection delay for streaming applications.
- Test changing normal behavior and rare anomalies.
- Tune alert thresholds to an acceptable false-alarm burden.
- Assess whether the model can distinguish novel attacks from known anomalies.

Metrics: PR-AUC when suitable labels exist, precision at a fixed alert budget, recall at a target false-positive rate, event-level detection, and detection delay.

## 5.3 Semi-supervised and self-supervised learning

These approaches learn from unlabeled data, limited labels, or automatically constructed learning targets.

Best practices

- Establish a fully supervised baseline using the available labeled data.
- Verify that unlabeled data does not contain evaluation leakage.
- Test sensitivity to incorrect pseudo-labels.
- Track the quality of pseudo-labels over training iterations.
- Compare learned representations using downstream tasks.
- Test whether additional unlabeled data improves performance rather than assuming that it does.
- Evaluate on independent labeled data.

Metrics: downstream task metrics, representation quality, label efficiency, and robustness to noisy pseudo-labels.

## 5.4 Transfer learning and domain adaptation

Transfer learning reuses learned representations or model parameters. Domain adaptation addresses differences between the source and target distributions.

Best practices

- Confirm that the source model is suitable for the target domain.
- Compare frozen feature extraction, partial fine-tuning, and full fine-tuning.
- Inspect negative transfer: pretraining can sometimes hurt performance.
- Avoid using target-test data to select adaptation strategies.
- Evaluate on the actual target domain.
- Measure how much labeled target data is required.
- Assess whether adaptation degrades performance on the original domain.

Metrics: target-domain performance, source-domain regression, sample efficiency, and robustness across domains.

## 5.5 Graph machine learning

Graph models learn from entities and their relationships.

Applications include social networks, molecular prediction, fraud detection, knowledge graphs, and recommendation.

Model families: graph neural networks, graph attention networks, graph transformers, and graph embedding methods.

Best practices

- Define the graph construction process and edge semantics.
- Prevent label, edge, and neighborhood leakage.
- Select splits based on whether the task concerns unseen nodes, unseen edges, or unseen graphs.
- Evaluate temporal graphs using realistic temporal cutoffs.
- Test robustness to missing, noisy, or adversarial edges.
- Consider graph size and inference scalability.
- Distinguish transductive from inductive generalization.

Metrics: task-specific AUC, F1, ranking metrics, link-prediction metrics, and generalization performance on held-out graphs or nodes.

## 5.6 Reinforcement learning

Reinforcement learning optimizes behavior through interaction with an environment or a learned simulator.

Model families: Q-learning, DQN, PPO, SAC, model-based RL, and offline RL.

Best practices

1. Define rewards and constraints carefully; unintended reward incentives can produce undesirable behavior.
2. Validate the simulator before trusting simulated results.
3. Run multiple random seeds and report variability.
4. Evaluate against simple policies and established baselines.
5. Test exploration and behavior under unfamiliar states.
6. For offline RL, assess distribution shift between logged actions and learned policies.
7. Evaluate safety constraints and worst-case outcomes.
8. Avoid deploying an experimental policy without appropriate safeguards.

Metrics: average return, success rate, regret, sample efficiency, constraint violations, and robustness across environments.

## 5.7 Online learning and continual learning

These systems update as new data arrives.

Best practices

- Track changes in input and target distributions.
- Define how labels become available and how delayed outcomes are handled.
- Evaluate performance continuously on appropriately timed observations.
- Prevent catastrophic forgetting of previously learned capabilities.
- Keep independent regression tests.
- Use staged deployment and rollback.
- Do not automatically retrain on every new batch without quality checks.

Metrics: prequential performance, adaptation speed, retained performance, drift recovery, and resource cost.

# Part 6. Generative AI and synthetic data

Generative models are evaluated differently from ordinary predictive models. Producing realistic samples is not enough: the samples must be appropriate, diverse, faithful to their conditioning inputs, and safe for the intended application.

## 6.1 Image and video generation

Best practices

- Separate realism, diversity, prompt adherence, temporal consistency, and artifact analysis.
- Evaluate memorization and training-data reproduction.
- Test rare concepts and challenging prompts.
- Check consistency across frames in video generation.
- Assess demographic and domain biases.
- Use human evaluation where automated metrics do not capture the intended quality.

Metrics: FID, precision/recall for generative distributions, perceptual similarity, human preference, prompt adherence, and temporal consistency.

## 6.2 Generative audio

Includes speech synthesis, music generation, sound effects, and audio transformation.

Best practices

- Evaluate sound quality and conditioning adherence independently.
- Check artifacts, clipping, timing, and long-range coherence.
- Test speaker consistency when identity is part of the task.
- Measure diversity without rewarding meaningless variation.
- Assess consent, rights, and misuse risks.

Metrics: task-specific perceptual quality, human preference, intelligibility, speaker similarity where relevant, and objective audio measures appropriate to the task.

## 6.3 Synthetic data generation

Synthetic data may be produced for privacy-sensitive analytics, simulation, model training, or rare-event augmentation.

Best practices

- Compare statistical distributions with the source data.
- Check preservation of important feature relationships.
- Test privacy leakage and memorization.
- Verify that synthetic rare events are realistic.
- Evaluate utility through downstream models.
- Compare against training with real data alone.
- Document whether generated samples are permitted for the intended use.

Metrics: distributional similarity, downstream utility, coverage of rare patterns, privacy evaluation, and domain-specific validity.

Synthetic data should not be treated as trustworthy simply because it looks realistic or resembles the training distribution.

# Part 7. Scientific, medical, and engineering ML

These applications require additional emphasis on physical plausibility, measurement uncertainty, external validation, and domain-specific failure modes.

## 7.1 Scientific machine learning

Examples include molecular property prediction, material discovery, astronomy, climate modeling, and scientific surrogate models.

Best practices

- Validate data provenance, units, coordinate systems, and measurement conditions.
- Prevent experimental replicates from leaking across splits.
- Evaluate out-of-distribution generalization.
- Quantify predictive uncertainty.
- Compare against established scientific models.
- Test known invariances and physical constraints.
- Verify results against independent experiments when feasible.

Metrics: predictive error, uncertainty calibration, constraint violations, scientific validity, and experimental agreement.

## 7.2 Physics-informed machine learning

Combines data-driven learning with physical laws, differential equations, or conservation constraints.

Best practices

- Validate the numerical implementation of governing equations.
- Balance data losses and physics-based losses carefully.
- Check boundary and initial conditions.
- Test whether the model satisfies constraints outside the training points.
- Evaluate sensitivity to measurement noise and discretization.
- Compare against numerical solvers and established baselines.

Metrics: solution error, residual norms, conservation-law violations, boundary-condition error, and computational efficiency.

A small training loss does not guarantee that a learned solution is physically correct.

## 7.3 Medical prediction and clinical AI

Beyond the vision-specific tasks discussed earlier, clinical AI includes prognosis, risk prediction, treatment support, physiological time-series modeling, clinical NLP, and multimodal patient modeling.

Best practices

- Define the intended clinical use and relevant patient population.
- Use patient-level and temporal leakage controls.
- Validate across institutions and relevant demographic subgroups.
- Assess calibration and clinically consequential errors.
- Account for prevalence changes between development and deployment.
- Document limitations, missing-data handling, and human oversight.
- Assess workflow impact and the consequences of incorrect predictions.
- Follow applicable clinical, privacy, and regulatory requirements.

Metrics: task-appropriate predictive metrics, calibration, confidence intervals, external validation performance, and decision-utility measures.

A model that performs well retrospectively may still fail when introduced into clinical practice because of changes in workflow, population, or data collection.

# Part 8. Additional machine learning task families

To make the handbook more complete, the following areas also deserve explicit treatment.

## 8.1 Dimensionality reduction and manifold learning

Tasks: compress features, visualize high-dimensional data, denoise representations, and reduce computational cost.

Best practices

- Compare against PCA and other simple baselines.
- Fit transformations on training data only.
- Evaluate information retention and downstream utility.
- Check stability across random seeds and parameter choices.
- Do not assume that a two-dimensional visualization preserves all high-dimensional relationships.

Metrics: explained variance, reconstruction error, neighborhood preservation, and downstream task performance.

## 8.2 Density estimation and generative probability modeling

Tasks: estimate the probability distribution of data, model uncertainty, and generate samples.

Best practices

- Select models suited to the data structure and dimensionality.
- Check numerical stability and distributional assumptions.
- Evaluate likelihood carefully; higher likelihood does not always mean better perceptual quality.
- Assess sample quality, coverage, and calibration where applicable.
- Test performance outside the central region of the training distribution.

Metrics: negative log-likelihood, held-out likelihood, CRPS for appropriate predictive distributions, and task-specific generative metrics.

## 8.3 Federated and privacy-preserving learning

Tasks: train across multiple organizations or devices without centrally collecting all raw data.

Best practices

- Evaluate non-IID client data and participation imbalance.
- Test communication failures and client availability.
- Assess whether global performance conceals poor local performance.
- Evaluate privacy risks, including gradient leakage and membership inference.
- Use differential privacy or secure aggregation when justified.
- Measure privacy–utility trade-offs rather than claiming that distributed training alone guarantees privacy.

Metrics: global and per-client performance, communication cost, convergence, and formal or empirical privacy measures.

## 8.4 Robotics and embodied AI

Tasks: perception, localization, motion planning, control, manipulation, and navigation.

Best practices

- Validate perception, planning, and control components separately.
- Test simulator-to-real transfer.
- Evaluate sensor noise, calibration drift, latency, and actuation constraints.
- Test recovery from unexpected states and environmental changes.
- Use safety constraints and emergency-stop mechanisms.
- Measure performance across complete tasks, not only individual model outputs.

Metrics: task completion rate, collision rate, control error, path efficiency, recovery success, and real-time latency.

## 8.5 Edge ML and model compression

Tasks: deploy models to mobile devices, embedded systems, cameras, and resource-constrained hardware.

Best practices

- Measure end-to-end latency on target hardware.
- Evaluate quantization, pruning, and distillation individually.
- Test accuracy degradation after conversion.
- Measure peak memory, energy use, startup time, and throughput.
- Validate numerical compatibility between training and deployment.
- Test hardware-specific behavior and fallback paths.

Metrics: task performance, latency percentiles, memory consumption, energy per inference, and model size.

## 8.6 Ensemble learning

Tasks: combine multiple models to improve accuracy, stability, or uncertainty estimates.

Best practices

- Compare against the strongest individual model.
- Verify that ensemble members make sufficiently complementary errors.
- Tune combination weights on validation data.
- Assess calibration and added computational cost.
- Test whether the ensemble improves independent-data performance.

Metrics: task-specific performance, calibration, variance across runs, latency, and memory.

# Part 9. Choosing the correct training objective

An important reason ML projects underperform is that the loss function does not match the actual goal.

| Task                      | Common training objectives                                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------- |
| Classification            | Cross-entropy, focal loss, task-specific cost-sensitive losses                              |
| Regression                | MSE, MAE, Huber loss, quantile loss                                                         |
| Semantic segmentation     | Cross-entropy, Dice loss, focal loss, boundary-aware losses                                 |
| Object detection          | Classification and localization losses, often with IoU-related objectives                   |
| Instance segmentation     | Detection losses plus mask-prediction losses                                                |
| Keypoint estimation       | Coordinate regression, heatmap losses, OKS-related objectives                               |
| Metric learning           | Contrastive loss, triplet loss, supervised contrastive loss                                 |
| Language modeling         | Next-token cross-entropy or other task-specific sequence objectives                         |
| Image generation          | Diffusion denoising objectives, adversarial losses, reconstruction or likelihood objectives |
| Ranking                   | Pairwise, listwise, or pointwise ranking objectives                                         |
| Survival analysis         | Partial likelihood, discrete-time survival losses, survival likelihood objectives           |
| Reinforcement learning    | Algorithm-specific value, policy, and return objectives                                     |
| Probabilistic forecasting | Negative log-likelihood, CRPS-related or quantile objectives                                |
| Causal inference          | Estimator-specific objectives, not merely generic predictive loss                           |

These are examples, not interchangeable recipes. A loss that improves optimization may not improve the evaluation metric or real-world objective.

## How to select a loss function properly

1. Define what constitutes a correct output.
2. Identify which errors matter most.
3. Choose an objective consistent with the output structure.
4. Verify that gradients and numerical behavior are stable.
5. Compare objective functions using the same experimental protocol.
6. Evaluate with the intended task metrics, not only the training loss.

For composite losses, document how components are weighted and test whether one component overwhelms the others.

# Part 10. Robustness, generalization, and failure analysis across all tasks

These are cross-cutting practices that should not be limited to classification.

## 10.1 Distribution-shift testing

Consider at least the relevant types of shift:

- Covariate shift: the input distribution changes.
- Label shift: the distribution of target classes changes.
- Concept drift: the relationship between inputs and targets changes.
- Domain shift: acquisition sites, users, environments, or operating conditions differ.
- Temporal shift: data characteristics evolve over time.
- Adversarial or malicious inputs: inputs are deliberately designed to exploit weaknesses.

Choose tests according to the intended deployment environment. Not every project needs every type of test.

## 10.2 Failure-mode analysis

Create a structured record for each major failure:

| Field               | What to record                                                   |
| ------------------- | ---------------------------------------------------------------- |
| Failure type        | Missed object, incorrect forecast, hallucination, drift, etc.    |
| Context             | Data source, conditions, and relevant subgroup                   |
| Root cause          | Data quality, model limitation, pipeline defect, or unknown      |
| Impact              | Consequences of the failure                                      |
| Proposed mitigation | Data collection, modeling change, threshold, or system safeguard |
| Verification        | Test demonstrating whether the fix works                         |

This helps prevent teams from repeatedly applying generic solutions to fundamentally different problems.

## 10.3 Statistical reliability

For every important comparison:

- Report sample sizes and the evaluation protocol.
- Estimate uncertainty using methods appropriate to the sampling structure.
- Use paired comparisons when models are evaluated on the same observations.
- Consider repeated seeds when training variability is important.
- Avoid selecting the best result from many experiments without accounting for selection bias.
- Report meaningful negative results and limitations.

For grouped or temporal data, confidence intervals must respect the dependence structure; treating every frame or measurement as independent can produce misleadingly narrow intervals.

# Part 11. Production ML engineering and MLOps

A high-performing model is not a complete ML system.

## 11.1 Recommended project architecture

```
ml-system/
├── configs/
├── data/
│   └── README.md
├── datasets/
│   └── manifests/
├── src/
│   ├── ingestion/
│   ├── validation/
│   ├── preprocessing/
│   ├── features/
│   ├── models/
│   ├── training/
│   ├── evaluation/
│   ├── inference/
│   ├── serving/
│   └── monitoring/
├── experiments/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── data/
│   └── model/
├── deployment/
├── reports/
├── pyproject.toml
└── README.md
```

The exact structure should be adapted to project size and deployment needs. Avoid turning every small experiment into a complex framework, but separate components that need independent testing, versioning, or reuse.

## 11.2 Required testing layers

Data tests

Schema validation, ranges, missingness, duplicates, labels, and leakage checks.

Unit tests

Preprocessing functions, transformations, loss calculations, and model utilities.

Integration tests

Data loading, preprocessing, training, checkpointing, and inference work together.

Model acceptance tests

The selected model meets predefined quality and performance requirements.

Serving tests

Input validation, latency, concurrency, memory use, and error handling.

Production monitoring

Input drift, delayed ground-truth metrics, system failures, and rollback behavior.

## 11.3 Model release checklist

Before a model is released:

- Confirm that its evaluation uses the intended final test protocol.
- Version the model, preprocessing, dependencies, and configuration together.
- Validate inference behavior against known test cases.
- Measure performance on the actual target hardware or serving environment.
- Document intended use, limitations, and known failure modes.
- Verify security, privacy, and access controls.
- Establish monitoring, rollback, and incident-response procedures.
- Define when retraining is justified and how a new model must be approved.

For reproducible experiments, useful tools include MLflow, DVC, Git, containerized environments, and automated testing. Tool selection should match the team's scale rather than become an objective in itself.

# Part 12. How to use this handbook for any new ML project

The practical goal is not to run every technique on every model. It is to select the relevant playbook and require evidence for each engineering decision.

## Choose a task-specific playbook

Select a domain and task to get a detailed implementation plan, including data preparation, architecture choices, training strategy, metrics, robustness tests, and deployment.

ML domainComputer vision

Specific taskSemantic segmentation

Project stage

Research prototype or academic paper

Production-grade ML system

Research and production

Generate detailed playbook

The central standard: Every ML task needs the same discipline in data integrity, reproducibility, experimental design, and honest evaluation—but each task must have its own appropriate architecture, objective function, metrics, validation strategy, and failure analysis.

This expanded handbook now covers the major task families, including detection, segmentation, tracking, keypoints, depth estimation, restoration, language modeling, forecasting, recommendation, causal inference, reinforcement learning, and generative systems. It can serve as the foundation for an even more detailed, task-by-task engineering manual.

## Applying this handbook to the medical-imaging project

The handbook is a source of decision criteria, not a requirement to implement
every technique or task. Apply the relevant principles to this project's
current 2D radiograph detection scope:

| Handbook principle | Project implementation |
|---|---|
| Define the task and intended claim before selecting a model | Keep box detection separate from image classification and mask segmentation. Record the study question, target ontology, primary metric, and intended generalization unit before opening an experiment. |
| Establish data provenance, schema, quality, and permission | Each `medimg.adapters` plugin owns source-specific validation. `medimg.loader` prepares a versioned artifact and records the source/config fingerprint. Keep raw data and generated artifacts out of Git. |
| Prevent leakage using the true independent unit | Preserve official dataset splits. Use patient/study-level grouping when identifiers exist; report limitations when grouping cannot be established. Never split annotation rows independently of images or patients. |
| Match preprocessing and augmentation to the task | Decode and canonicalize once during preparation. Apply stochastic transforms at training time, and require image/box geometry to remain aligned. Keep validation and test transforms deterministic. |
| Match the objective and metric to the output | Detection losses and box metrics are separate from classification and segmentation. For ChestX-Det10, preserve its low-FP-per-image native metric and report standardized AP only as a separately defined secondary metric. |
| Establish a baseline and keep comparisons controlled | Start with one documented detector/config. Change one study factor at a time for ablations; select checkpoints and thresholds on validation only. |
| Analyze failures and statistical uncertainty | Report per-class support and errors, seed-to-seed variation, and uncertainty at the patient/study level when grouping is available. Consider external/domain-shift tests only when the label mapping and data protocol support them. |
| Build layered tests and acceptance checks | Test contracts, adapters, transforms, metrics, then prepare-to-reader-to-model integration. A training run is not accepted until its data manifest, config, checkpoint, evaluator, and required metrics agree. |

These principles map to the current implementation and workflow in
[`detection_workflow.md`](detection_workflow.md) and
[`architecture_blueprint.md`](architecture_blueprint.md). In particular, the
prepare-first cache is the project-specific implementation of repeatable
preprocessing; it does not remove the need for provenance, split checks,
validation-only model selection, or independent final evaluation.

For the current phase, deployment serving, online learning, reinforcement
learning, and unrelated task families in this handbook are deliberately out
of scope. Add them only if the research question changes and the new task has
its own data, target, model, and evaluation contracts.