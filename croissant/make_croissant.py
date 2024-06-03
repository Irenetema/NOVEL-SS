# This software was created by Oregon State University under Army Research
# Office (ARO) Award Number W911NF-22-2-0149. ARO, as the Federal awarding
# agency, reserves a royalty-free, nonexclusive and irrevocable right to
# reproduce, publish, or otherwise use this software for Federal purposes, and
# to authorize others to do so in accordance with 2 CFR 200.315(b).

"""
Create croissant metadata
"""
import os
import argparse
import json

from etils import epath

from croissant.combine_annotations_to_json import merge_annotations_n_bbox
from croissant.croissant_format_novel_ss import croissant_format


def main():
    parser = argparse.ArgumentParser(
        description='Combine NOVEL SS labels (csv) and bounding boxes in to one json file'
    )
    parser.add_argument(
        '--path_to_zipped_labels',
        default='labels/novel_ss_labels.zip',
        help='Path to NOVEL SS zipped labels and bounding box object'
    )
    parser.add_argument(
        '--output_dir',
        default='labels/cr_json_annotations/',
        help='Path to dir where to save the combined labels'
    )

    args = parser.parse_args()

    assert os.path.exists(args.path_to_zipped_labels)

    # Merge NOVEL-SS annotations and bounding box into a single json, and
    # create a zip obj of the json files for train, validation and test sets
    if not os.path.exists(args.output_dir):
        merge_annotations_n_bbox(args.path_to_zipped_labels, args.output_dir)

    # create croissant metadata
    metadata = croissant_format()

    jsonld = epath.Path("croissant.json")
    with jsonld.open("w") as f:
        f.write(json.dumps(metadata.to_json(), indent=2))

    # !grep -C 7 -n "cr:BoundingBox" croissant.json

    # ******* Print sample ********
    import mlcroissant as mlc
    dataset = mlc.Dataset(jsonld=jsonld)
    records = dataset.records(record_set="images_and_bbox")
    record = next(iter(records))
    print("The first record:")
    print(json.dumps(record, indent=2))
    




if __name__ == "__main__":
    main()
