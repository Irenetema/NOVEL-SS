# NOVEL-SS: A Dataset for Integrated Novelty-Aware Computer Vision Systems 

* NOVEL-SS
![NOVEL-SS Novelty Categories](/create_novel_ss/sample_images.jpg)


## Download the NOVEL-SS images
0. Clone this [NOVEL-SS repository](https://github.com/Irenetema/NOVEL_SS)
1. Extract the annotations [labels/novel_ss_labels.zip](/labels/novel_ss_labels.zip)
2. Download the training, validation and test images  
   Run: `python -m download_novel_ss.download_novel_ss_images --labels_dir 'PATH/TO/EXTRACTED/LABELS' --output_dir 'DIR/WHERE/TO/SAVE/IMAGES'`
3. Create artificial novel environments (select a subset of the training set and apply transformations to simulate fog and snow effects)  
    Run: `python -m download_novel_ss.create_artificial_envs --labels_dir 'PATH/TO/EXTRACTED/LABELS' --images_dir 'DIR/WHERE/DOWNLOADED/IMAGES/ARE/SAVED'`  
    (images_dir should be the same as 'DIR/WHERE/TO/SAVE/IMAGES' provided when downloading the images)


## DCA (Detect-Characterize-Accommodate) baseline for NOVEL-SS
1. Get SS server side system https://github.com/guyera/ss-api
2. Get SS client side system https://github.com/guyera/ss-osu-system
3. Generate validation and test trials from the NOVEL-SS labels (follow the steps in https://github.com/guyera/ss-osu-system/tree/master/umd_test_generate)


## NOVEL-SS Dataset Creation (from the Snapshot Serengeti Cameratrap)

![NOVEL-SS Creation process](/create_novel_ss/NOVEL-SS_Flowchart.jpg)

- Steps:
1. Filter [Snapshot Serengeti](https://lila.science/datasets/snapshot-serengeti) dataset annotation to select all images satisfying the NOVEL-SS novelty types definition.  
`python -m create_novel_ss.label_filtering --path_ss_annotations '/PATH/TO/SS/ANNOTATIONS/SnapshotSerengeti_v2_1_annotations.csv' --path_ss_images_url '/PATH/TO/SS/ANNOTATIONS/SnapshotSerengeti_v2_1_images.csv' --output_dir '/PATH/TO/SAVE/LABELS/OF/QUALIFYING_IMAGES/'`

2. Run Microsoft's MegaDetector on the selected images to extract the bounding boxes information and the count of animals in each images. Follow the steps at https://github.com/Irenetema/megadetector to install and run the MegaDetector on selected images (this is a fork of [Microsoft's MegaDetector repository](https://github.com/microsoft/CameraTraps/tree/main/archive)).

3. 




## Disclosure
This data was produced by Oregon State University under Army Research Office (ARO) Award Number W911NF-22-2-0149. ARO, as the Federal awarding agency, reserves a royalty-free, nonexclusive 
and irrevocable right to reproduce, publish, or otherwise use this data for Federal purposes, and to authorize others to do so in accordance with 2 CFR 200.315(b).
