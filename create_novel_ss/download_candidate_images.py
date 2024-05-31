# This software was created by Oregon State University under Army Research
# Office (ARO) Award Number W911NF-22-2-0149. ARO, as the Federal awarding
# agency, reserves a royalty-free, nonexclusive and irrevocable right to
# reproduce, publish, or otherwise use this software for Federal purposes, and
# to authorize others to do so in accordance with 2 CFR 200.315(b).

"""
Download candidate images after label filtering
"""

import os
import argparse
import pandas as pd
from pathlib import Path

from config.config import NOVELTY_TYPES
from utils.download_images import download


def main():
    parser = argparse.ArgumentParser(
        description='Download selected images for each novelty type'
    )
    parser.add_argument(
        '--labels_dir',
        default='PATH_TO_CANDIDATE_IMAGES/labels/',
        help='Path to SS dataset annotations csv file (sequence level annotations)'
    )
    parser.add_argument(
        '--output_dir',
        help='Directory for output images (defaults to same as input)'
    )

    args = parser.parse_args()

    assert os.path.exists(args.labels_dir), '* labels_dir {} does not exist!'.format(args.labels_dir)
    assert os.path.exists(args.output_dir), '* Output directory {} does not exist!'.format(args.output_dir)

    # download selected images
    for novelty_type in NOVELTY_TYPES:
        label_path = os.path.join(args.labels_dir, f'{novelty_type}_labels.csv')
       
        assert os.path.exists(label_path)

        output_dir_novelty = os.path.join(args.output_dir, f'{novelty_type}_labels.csv')
        Path(output_dir_novelty).mkdir(parents=True, exist_ok=True)

        image_labels = pd.read_csv(label_path)

        list_image_urls = image_labels['image_path_rel'].drop_duplicates().to_list()

        print('*** Downloading images for:', novelty_type, 'novelty type...')
                
        download(list_image_urls, output_dir_novelty, novelty_type)


if __name__ == "__main__":
    main()
    
