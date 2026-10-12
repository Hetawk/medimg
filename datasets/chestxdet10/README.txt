ChestX-Det10 dataset notes
=========================

Downloaded: 2026-10-08
Local project: labcode/medical
Dataset: ChestX-Det10, a chest-X-ray object-detection dataset

What this dataset contains
--------------------------
The dataset authors describe ChestX-Det10 as a 3,543-image subset of NIH
ChestX-ray14 with instance-level bounding-box annotations. Three
board-certified radiologists annotated ten thoracic abnormality classes:

  Atelectasis, Calcification, Consolidation, Effusion, Emphysema, Fibrosis,
  Fracture, Mass, Nodule, Pneumothorax

The released split represented here has:

  Training: 3,001 images and annotation entries
  Test:       542 images and annotation entries
  Total:    3,543 images and annotation entries

Annotation format
-----------------
JSON annotations are in annotations/train.json and annotations/test.json.
Each entry contains:

  file_name: image filename
  syms:      class names
  boxes:     [x1, y1, x2, y2] coordinates (top-left, bottom-right)

The authors' README describes train.json and test.json and provides eval.py
for their challenge evaluation protocol. The challenge metric is recall at
fixed false positives per image (0.05, 0.1, and 0.2), with a positive
prediction IoU threshold of 0.5. Do not assume this is identical to mAP;
state the chosen evaluation protocol in any report.

Local files
-----------

  train_data.zip                 1,210,114,616 bytes
  test_data.zip                    218,238,743 bytes
  annotations/train.json             394,030 bytes
  annotations/test.json               79,457 bytes

The image ZIP archives passed `unzip -t` integrity checks. Their image counts
match the annotation entry counts. Archives are kept zipped.

SHA-256 checksums
-----------------

  train_data.zip
  165b2749b8f245ea2b3cdffb45409f8a88612f4eb956b44a3f3d769f9a5e89e5

  test_data.zip
  7182cbe9a0f1b435139ba4243cf7ea0e47b5f977b6c610716d045e146c201d31

  annotations/train.json
  8e9dd7123bdd9e5ce8d8cd7bd304fd24afdf0081930654b82c2003422d59de9c

  annotations/test.json
  c18482a77111186789c67d836db27a522c717cdb638eff59bc463362a60a46f1

Sources
-------

Dataset authors' repository and dataset instructions:
  https://github.com/Deepwise-AILab/ChestX-Det10-Dataset

Image archive URLs specified by the authors:
  http://resource.deepwise.com/xraychallenge/train_data.zip
  http://resource.deepwise.com/xraychallenge/test_data.zip

Dataset paper:
  Jingyu Liu, Jie Lian, and Yizhou Yu.
  "ChestX-Det10: Chest X-ray Dataset on Detection of Thoracic Abnormalities."
  arXiv:2006.10550, 2020.
  https://arxiv.org/abs/2006.10550

The authors describe these images as a subset of NIH ChestX-ray14:
  https://nihcc.app.box.com/v/ChestXray-Nihcc

Reuse and attribution
--------------------
The dataset authors' repository does not provide an explicit license file or
license grant in its README. The images originate from NIH ChestX-ray14, so
review the applicable NIH source-data terms and cite both the dataset paper
and its source dataset before research use or redistribution. Public
downloadability is not by itself a reuse license. Do not publish or upload
the image archives or derived patient-level data to a public repository
without confirming permission.

Citation (from the authors' repository)
--------------------------------------

@misc{liu2020chestxdet10,
  title={ChestX-Det10: Chest X-ray Dataset on Detection of Thoracic Abnormalities},
  author={Jingyu Liu and Jie Lian and Yizhou Yu},
  year={2020},
  eprint={2006.10550v3},
  archivePrefix={arXiv},
  primaryClass={eess.IV}
}
