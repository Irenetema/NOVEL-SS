# Downloading NOVEL-SS Dataset 

## Steps to download the NOVEL-SS images from the Snapshot Serengeti dataset
0. Clone this NOVEL-SS repository
1. Extract the annotations 'labels/novel_ss_labels.zip'
2. Download the training, validation and test images
    Run: `python -m download_novel_ss.download_novel_ss_images --labels_dir 'PATH/TO/EXTRACTED/LABELS' --output_dir 'DIR/WHERE/TO/SAVE/IMAGES'`
3. Create artificial novel environments (select a subset of the training set and apply transformations to simulate fog and snow effects)
    Run: `python -m download_novel_ss.create_artificial_envs --labels_dir 'PATH/TO/EXTRACTED/LABELS' --images_dir 'DIR/WHERE/DOWNLOADED/IMAGES/ARE/SAVED'`
    (images_dir should be the same as 'DIR/WHERE/TO/SAVE/IMAGES' provided when downloading the images)


# DCA (Detect-Characterize-Accommodate) baseline for NOVEL-SS
1. Get SS server side system https://github.com/guyera/ss-api
2. Get SS client side system https://github.com/guyera/ss-osu-system
3. Generate validation and test trials from the NOVEL-SS labels (follow the steps in https://github.com/guyera/ss-osu-system/tree/master/umd_test_generate)


# NOVEL-SS Dataset Creation from the Snapshot Serengeti Cameratrap
- Process
![NOVEL-SS Creation process](/create_novel_ss/NOVEL-SS_Flowchart.jpg)

- Steps:
1. run the script initial_candidate_imgs_selection.py to analyze the Snapshot Serengeti and select all images belonging to the known (prenovelty) and novelty types.
`python -m create_novel_ss.label_filtering --path_ss_annotations '/PATH/TO/SS/ANNOTATIONS/SnapshotSerengeti_v2_1_annotations.csv' --path_ss_images_url '/PATH/TO/SS/ANNOTATIONS/SnapshotSerengeti_v2_1_images.csv' --output_dir '/PATH/TO/SAVE/LABELS/OF/QUALIFYING_IMAGES/'`

2. Run the MegaDetector (megadetector/cameratraps/detection/run_detector.py) on the pre-selected images to count the number of animals in each images. Then discard images for which the detection count does not match the ground truth labels for Snapshot Serengeti. Follow the steps at https://github.com/Irenetema/megadetector to install the required packages and depencies needed to run the MegaDetector (this is a fork of Microsoft's MegaDetector repository at https://github.com/microsoft/CameraTraps/tree/main/archive)

3. 


****************************************************
Steps:
* a. Run initial_candidate_imgs_selection.py to filter images that do not match any of the novelty types definition (set the variable "download_candidate_imgs" to True to download the selected candidate images)
* b. Run megadetector/cameratraps/detection/run_detector.py to extract the bounding boxes of the candidate images from a. using the megadetector.
* c. Run build_trials/generate_final_novelty_csv_n_json.py to assemble the csv files and corresponding bounding boxes to be used for building the training, validation and test sets for the SAILON task
* d. Run create_train_valid_test_sets.py to create the finale CSVs and JSONs files used for training the models and also used for building the trials.



