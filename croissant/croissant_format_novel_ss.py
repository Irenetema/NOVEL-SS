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
            id="jsonl-files",
            name="jsonl-files",
            description="NOVEL-SS training set image annotations.",
            content_url="https://raw.githubusercontent.com/Irenetema/NOVEL_SS/master/labels/croissant_jsonl.zip",
            encoding_format="application/zip",
            sha256="63aa31303b1157cfc35ced7bbb643904834bb1ad7ba4d1cb99fc4fa03a7c044c",
        ),
        mlc.FileObject(
            id="train_annotations",
            name="train_annotations",
            description="NOVEL-SS training set image annotations.",
            contained_in=["jsonl-files"],
            content_url="train.jsonl",
            encoding_format="application/jsonlines"
        ),
        mlc.FileObject(
            id="valid_annotations",
            name="valid_annotations",
            description="NOVEL-SS training set image annotations.",
            contained_in=["jsonl-files"],
            content_url="valid.jsonl",
            encoding_format="application/jsonlines"
        ),
        mlc.FileObject(
            id="test_annotations",
            name="test_annotations",
            description="NOVEL-SS training set image annotations.",
            contained_in=["jsonl-files"],
            content_url="test.jsonl",
            encoding_format="application/jsonlines"
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
                    description="Snapshot Serengeti image path (e.g. S6/P07/P07_R2/S6_P07_R2_IMAG0077.JPG)",
                    data_types=mlc.DataType.TEXT,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="image_path"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/image_bboxes",
                    name="image_bboxes",
                    description="bounding boxes of animal position in each images. [will update data_types=mlc.DataType.BOUNDING_BOX(mlc.Context())]",
                    data_types=mlc.DataType.TEXT,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="bboxes"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/filename",
                    name="filename",
                    description="Snapshot Serengeti image name (e.g. S6_P07_R2_IMAG0077.JPG)",
                    data_types=mlc.DataType.TEXT,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="filename"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/capture_id",
                    name="capture_id",
                    description="Snapshot Serengeti image sequence id (e.g., SER_S6#P07#2#29)",
                    data_types=mlc.DataType.TEXT,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="capture_id"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/width",
                    name="width",
                    description="Image width (e.g., 2048)",
                    data_types=mlc.DataType.INTEGER,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="width"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/height",
                    name="height",
                    description="Image height (e.g., 1536)",
                    data_types=mlc.DataType.INTEGER,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="height"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/agent1_name",
                    name="agent1_name",
                    description="Name of animal species 1 (e.g., zebra)",
                    data_types=mlc.DataType.TEXT,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="agent1_name"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/agent1_id",
                    name="agent1_id",
                    description="Id of animal species 1 (integer between 1 and 30)",
                    data_types=mlc.DataType.INTEGER,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="agent1_id"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/agent1_count",
                    name="agent1_count",
                    description="number of animals from species 1",
                    data_types=mlc.DataType.INTEGER,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="agent1_count"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/agent2_name",
                    name="agent2_name",
                    description="Name of animal species 2 (None if image contains only 1 species)",
                    data_types=mlc.DataType.TEXT,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="agent2_name"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/agent2_id",
                    name="agent2_id",
                    description="Id of animal species 2 (None if image contains only 1 species)",
                    data_types=mlc.DataType.INTEGER,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="agent1_id"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/agent2_count",
                    name="agent2_count",
                    description="number of animals from species 2",
                    data_types=mlc.DataType.INTEGER,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="agent2_count"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/agent3_name",
                    name="agent3_name",
                    description="Name of animal species 3 (None if image contains only 1 species)",
                    data_types=mlc.DataType.TEXT,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="agent3_name"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/agent3_id",
                    name="agent3_id",
                    description="Id of animal species 3 (None if image contains only 1 species)",
                    data_types=mlc.DataType.INTEGER,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="agent3_id"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/agent3_count",
                    name="agent1_count",
                    description="number of animals from species 3",
                    data_types=mlc.DataType.INTEGER,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="agent3_count"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/activities",
                    name="activities",
                    description="list of animal activities",
                    data_types=mlc.DataType.TEXT,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="activities"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/activities_id",
                    name="activities_id",
                    description="list of ids of animal activities",
                    data_types=mlc.DataType.TEXT,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="activities_id"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/environment_id",
                    name="environment_id",
                    description="id of environment (lighting condition) of the image",
                    data_types=mlc.DataType.INTEGER,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="environment_id"),
                    ),
                ),
                mlc.Field(
                    id="images_and_bbox/novelty_type",
                    name="novelty_type",
                    description="interger indentifying the type of novelty in the image",
                    data_types=mlc.DataType.INTEGER,
                    source=mlc.Source(
                        file_object="train_annotations",
                        extract=mlc.Extract(column="novelty_type"),
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
            "Novel-Snapshot Serengeti (Novel-SS), is a benchmark derived from the"
            " Snapshot Serengeti camera trap dataset collected by a network of 225 camera traps"
            " deployed in Serengeti National Park (Tanzania). NOVEL-SS offers many forms of novelty"
            " including: novel species, novel activity, novel combination of species, novel combination"
            "of activities, and novel environment (e.g. dawn, dusk, night time, snow and fog)."
        ),
        cite_as=(
            "@misc{tematelewo2024novelss, title={Novel-SS: A Benchmark for Integrated Novelty-Aware"
            " Computer Vision Systems}, author={Tematelewo, Iren\'e and Ullah, Amin and Guyer Alexander"
            " and Fuxin, Li and Lee, Stefan and Dietterich, Thomas G}, booktitle = {openreview},"
            " month = {June}, year = {2024},"
        ),
        distribution=distribution,
        record_sets=record_sets,
        url="https://github.com/Irenetema/NOVEL_SS",
        version="1.0",
        license="GPL-3.0",
    )

    return metadata
