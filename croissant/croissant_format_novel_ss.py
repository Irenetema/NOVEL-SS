# This software was created by Oregon State University under Army Research
# Office (ARO) Award Number W911NF-22-2-0149. ARO, as the Federal awarding
# agency, reserves a royalty-free, nonexclusive and irrevocable right to
# reproduce, publish, or otherwise use this software for Federal purposes, and
# to authorize others to do so in accordance with 2 CFR 200.315(b).


# !pip install --only-binary :all jsonpath-rw
# !pip install "git+https://github.com/${GITHUB_REPOSITORY:-mlcommons/croissant}.git@${GITHUB_HEAD_REF:-main}#subdirectory=python/mlcroissant&egg=mlcroissant[dev]"

import mlcroissant as mlc


def croissant_format():
    # FileObjects and FileSets define the resources of the dataset.
    distribution = [
        # NOVEL-SS annotations:
        mlc.FileObject(
            id="novel_ss_annotations",
            name="novel_ss_annotations",
            description="NOVEL-SS training, validation and test image annotations.",
            content_url=("https://github.com/Irenetema/NOVEL_SS/blob/master/labels/novel_ss_labels.zip"),
            encoding_format="application/zip",
            sha256="main",
        ),
        # *** Image annotations ***
        # training set annotations:
        mlc.FileObject(
            id="train_annotations",
            name="train_annotations",
            description="NOVEL-SS training set image annotations.",
            contained_in=["novel_ss_annotations"],
            content_url="train.json",
            encoding_format="application/json"
        ),
        # validation set annotations:
        mlc.FileObject(
            id="valid_annotations",
            name="valid_annotations",
            description="NOVEL-SS validation set image annotations.",
            contained_in=["novel_ss_annotations"],
            content_url="valid.json",
            encoding_format="application/json"
        ),
        # test set annotations:
        mlc.FileObject(
            id="test_annotations",
            name="test_annotations",
            description="NOVEL-SS test set image annotations.",
            contained_in=["novel_ss_annotations"],
            content_url="test.json",
            encoding_format="application/json"
        ),
    ]

    record_sets = [
        # RecordSets contains records in the dataset.
        mlc.RecordSet(
            id="images_and_bbox",
            name="images_and_bbox",
            fields=[
                mlc.Field(
                    id="images_and_bbox/image_path",
                    name="image_path",
                    description="",
                    data_types=mlc.DataType.TEXT,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(json_path="$..image_path"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/image_bboxes",
                    name="image_bboxes",
                    description="",
                    data_types=mlc.DataType.BOUNDING_BOX(mlc.Context()),
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(json_path="$..bboxes"),
                    ),
                ),
            ],
        ),
    ]

    # Metadata contains information about the dataset.
    metadata = mlc.Metadata(
        name="NOVEL-SS",
        # Descriptions can contain plain text or markdown.
        description=(
            "Most deployed computer vision systems encounter a wide variety of"
            " novel situations. Computer vision researchers have studied many kinds of" 
            " novelty separately including changes in object appearance and style, changes in"
            " class distribution, novel object classes, novel activities, and novel imaging"
            " conditions. To detect and respond to these novelties, various techniques have"
            " been developed including novelty detection, invariant feature discovery, meta"
            " learning, transfer learning, active learning, continual learning, domain"
            " adaptation, and so on. Benchmarks corresponding to each of these problems and"
            " techniques have been developed. This paper argues that it is time for the field to"
            " integrate these various novelty detection and accommodation techniques into a"
            " single system that can detect and accommodate many types of novelty. To"
            " promote this effort, we introduce Novel-Snapshot Serengeti (Novel-SS), a"
            " benchmark derived from the Snapshot Serengeti camera trap dataset collected by a"
            " network of 225 camera traps deployed in Serengeti National Park (Tanzania). In this"
            " application, many forms of novelty arise. In our Novel-SS protocol, the vision system has"
            " the option to request annotations for individual images, which allows it to obtain a small"
            " amount of supervised data through active learning. The overall goal is to maximize task"
            " performance while minimizing the number of requested annotations. This paper describes the"
            " training data, performance task, types of novelty, evaluation protocol, and evaluation"
            " metrics. To demonstrate the feasibility of the task, we present a novelty-aware"
            " system, DCA-SS, and compare it to a baseline system that is completely unaware of novelty."
        ),
        cite_as=(
            "@misc{tematelewo2024novelss, title={Novel-SS: A Benchmark for Integrated Novelty-Aware"
            " Computer Vision Systems}, author={Tematelewo, Iren\'e and Ullah, Amin and Guyer Alexander"
            " and Fuxin, Li and Lee, Stefan and Dietterich, Thomas G}, booktitle = {openreview},"
            " month = {June}, year = {2024},"
        ),
        url="https://github.com/Irenetema/NOVEL_SS",
        distribution=distribution,
        record_sets=record_sets,
    )

    return metadata
