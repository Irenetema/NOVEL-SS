# Downloading NOVEL-SS Dataset 

* Steps to download the NOVEL-SS images from the Snapshot Serengeti dataset
0. Clone this NOVEL-SS repository
1. Extract the annotations 'labels/novel_ss_labels.zip'
2. Download the training, validation and test images
    Run: python -m download_novel_ss.download_novel_ss_images --labels_dir 'PATH/TO/EXTRACTED/LABELS' --output_dir 'DIR/WHERE/TO/SAVE/IMAGES'
3. Create artificial novel environments (select a subset of the training set and apply transformations to simulate fog and snow effects)
    Run: python -m download_novel_ss.create_artificial_envs --labels_dir 'PATH/TO/EXTRACTED/LABELS' --images_dir 'DIR/WHERE/DOWNLOADED/IMAGES/ARE/SAVED'
    (images_dir should be the same as 'DIR/WHERE/TO/SAVE/IMAGES' provided when downloading the images)


# DCA (Detect-Characterize-Accommodate) baseline for NOVEL-SS
1. Get SS server side system https://github.com/guyera/ss-api
2. Get SS client side system https://github.com/guyera/ss-osu-system
3. Generate validation and test trials from the NOVEL-SS labels (follow the steps in https://github.com/guyera/ss-osu-system/tree/master/umd_test_generate)


# NOVEL-SS Dataset Creation from the Snapshot Serengeti Cameratrap




