"""
Download NOVEL-SS images
"""

import os
import argparse
import pandas as pd
from pathlib import Path

from utils.download_images import download


def make_ss_url(file_name):
    """
    Format image name as compatible for Snapshot Serengeti (SS)
    Argument:
        file_name (str): name of the image 
        (e.g. train/S7_S07_R3_IMAG0195.JPG or train/SER_S11_G04_R1_IMAG1028R.JPG)
    Return (str): valid SS url 
    (e.g. S7/S07_R3/S7_S07_R3_IMAG0195.JPG or SER_S11/G04/G04_R1/SER_S11_G04_R1_IMAG1028.JPG)
    """
    f_name = file_name.split('/')[-1]
    list_parts = f_name.split('_')
    if len(list_parts) == 4:
        return list_parts[0] + '/' + list_parts[1] + '/' + list_parts[1] + '_' + list_parts[2] + '/' + f_name
    return list_parts[0] + '_' + list_parts[1] + '/' + list_parts[2] + '/' + list_parts[2] + '_' + list_parts[3] + '/' + f_name


def main():
    parser = argparse.ArgumentParser(
        description='Download NOVEL-SS train, validation and test images'
    )
    parser.add_argument(
        '--labels_dir',
        help='Path to extracted directory containing labels train.csv, valid.csv and test.csv'
    )
    parser.add_argument(
        '--output_dir',
        help='Directory for output images (defaults to same as input)'
    )

    args = parser.parse_args()

    assert os.path.exists(args.labels_dir), '* labels_dir {} does not exist!'.format(args.labels_dir)
    assert os.path.exists(args.output_dir), '* Output directory {} does not exist!'.format(args.output_dir)

    # download selected images
    for dataset in ['train.csv', 'valid.csv', 'test.csv']:
        label_path = os.path.join(args.labels_dir, dataset)
       
        assert os.path.exists(label_path)

        image_labels = pd.read_csv(label_path)
        image_labels = image_labels['image_path']

        dataset_output_dir = image_labels.to_list()[0].split('/')[0]
        output_dir = os.path.join(args.output_dir, dataset_output_dir)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)   

        print(f'*** Downloading {dataset.split(".")[0]} set images...')

        # build snapshot serengeti images url from file names
        list_image_urls = image_labels.apply(make_ss_url)
                
        download(list_image_urls, output_dir, novelty_type=None)


if __name__ == "__main__":
    main()
    