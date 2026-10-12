RSNA Pneumonia Detection Challenge dataset
=========================================

Downloaded: 2026-10-08
Local project: labcode/medical
Dataset: RSNA Pneumonia Detection Challenge 2018, Stage 2

What this dataset contains
--------------------------
The Kaggle challenge archive contains 26,684 training chest radiographs in
DICOM format, with pneumonia labels and bounding boxes in
stage_2_train_labels.csv. It also contains 3,000 test DICOM images. Test
labels are not included in the public competition archive.

For a negative study, the training CSV has Target=0 and blank box fields.
Positive images may have multiple rows/boxes. The archive also includes
stage_2_detailed_class_info.csv and stage_2_sample_submission.csv.

Local files
-----------

  rsna-pneumonia-detection-challenge.zip  3,932,287,530 bytes

The archive passed `unzip -t` with no compressed-data errors. It contains
26,684 training DICOMs and 3,000 test DICOMs. It is kept zipped.

SHA-256
-------

  rsna-pneumonia-detection-challenge.zip
  133acacf95aa68c4d219124b17937f31cec073052096b9f9b122180df9d9af18

Sources
-------

Kaggle competition data and rules:
  https://www.kaggle.com/competitions/rsna-pneumonia-detection-challenge/data
  https://www.kaggle.com/competitions/rsna-pneumonia-detection-challenge/rules

RSNA challenge information:
  https://www.rsna.org/artificial-intelligence/ai-image-challenge/rsna-pneumonia-detection-challenge-2018

Reuse, access, and attribution
------------------------------
This dataset is distributed through a Kaggle competition and is governed by
the competition's rules and data-use terms; do not assume it has an
unrestricted open-data license. A collaborator should review and accept the
current rules and obtain the data through an authorized account rather than
receiving an unapproved copy. Do not upload the archive or derived
patient-level data to a public repository. Follow the competition's citation
and attribution instructions in any research output.

The training CSV uses patientId, x, y, width, height, and Target. Preserve
the supplied split and document any conversion from DICOM/CSV to a training
framework's image and box format.
