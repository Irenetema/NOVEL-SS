# This software was created by Oregon State University under Army Research
# Office (ARO) Award Number W911NF-22-2-0149. ARO, as the Federal awarding
# agency, reserves a royalty-free, nonexclusive and irrevocable right to
# reproduce, publish, or otherwise use this software for Federal purposes, and
# to authorize others to do so in accordance with 2 CFR 200.315(b).

"""
Add artificial image corruption to selected novel environments novelty types
"""

import os
import argparse
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm

from utils.corruptions import *
from config.config import ENVIRONMENTS_ID2NAME, ENV_CORRUPTION_SEVERITY

'''
corruption_tuple = (gaussian_noise, shot_noise, impulse_noise,
                    glass_blur, motion_blur, zoom_blur, snow, frost, fog,
                    brightness, contrast, elastic_transform, pixelate, jpeg_compression,
                    speckle_noise, gaussian_blur, spatter, saturate)
'''

corruption_tuple = (snow, fog)
corruption_dict = {corr_func.__name__: corr_func for corr_func in corruption_tuple}


def corrupt(x, severity=1, corruption_name=None, corruption_number=-1):
    """
    :param x: image to corrupt
    :param severity: strength with which to corrupt x; an integer in [0, 5]
    :param corruption_name: specifies which corruption function to call;
    must be one of 'gaussian_noise', 'shot_noise', 'impulse_noise', 'defocus_blur',
                    'glass_blur', 'motion_blur', 'zoom_blur', 'snow', 'frost', 'fog',
                    'brightness', 'contrast', 'elastic_transform', 'pixelate', 'jpeg_compression',
                    'speckle_noise', 'gaussian_blur', 'spatter', 'saturate';
                    the last four are validation functions
    :param corruption_number: the position of the corruption_name in the above list;
    an integer in [0, 18]; useful for easy looping; 15, 16, 17, 18 are validation corruption numbers
    :return: the image x corrupted by a corruption function at the given severity; same shape as input
    """

    if corruption_name:
        x_corrupted = corruption_dict[corruption_name](x, severity)
    elif corruption_number != -1:
        x_corrupted = corruption_tuple[corruption_number](x, severity)
    else:
        raise ValueError("Either corruption_name or corruption_number must be passed")

    return x_corrupted


def main():
    parser = argparse.ArgumentParser(
        description='Add corruption to subset of no-novelty/training set to create artificial novel environments snow and fog.'
    )
    parser.add_argument(
        '--labels_dir',
        help='Path to extracted directory containing labels train.csv, valid.csv and test.csv'
    )
    parser.add_argument(
        '--images_dir',
        help='Directory containing downloaded images (parent dir of train, valid and test folders)'
    )

    args = parser.parse_args()

    assert os.path.exists(args.labels_dir), '* labels_dir {} does not exist!'.format(args.labels_dir)
    assert os.path.exists(args.images_dir), '* Output directory {} does not exist!'.format(args.images_dir)

    # get id of all artificial environments novelty types
    artificial_envs = list(ENV_CORRUPTION_SEVERITY.keys())
    id_art_env = [int(env_id) for env_id, env_name in ENVIRONMENTS_ID2NAME.items() if env_name in artificial_envs]

    # download selected images
    for dataset in ['valid.csv', 'test.csv']:
        label_path = os.path.join(args.labels_dir, dataset)
       
        assert os.path.exists(label_path)

        image_labels = pd.read_csv(label_path)
        image_labels = image_labels.loc[image_labels['environment_id'].isin(id_art_env)]

        for corr_id in image_labels['environment_id'].unique():
            corr = ENVIRONMENTS_ID2NAME[str(corr_id)]

            print(f'>> [{dataset[:-4]}]: Creating artificial environment ** {corr} **')

            list_imgs_corr = image_labels['image_path'].loc[image_labels['environment_id'] == corr_id].to_list() 

            for img_fname in tqdm(list_imgs_corr):
                img_path = os.path.join(args.images_dir, img_fname)
                assert os.path.exists(img_path)
                image = Image.open(img_path)
                try:
                    img_corrupted = corrupt(
                        image, severity=ENV_CORRUPTION_SEVERITY[corr], 
                        corruption_name=corr, corruption_number=-1
                    )
                except Exception as ex:
                    print(f'The following exception happened: {ex}')
                    continue

                # convert the np array returned by "corrupt" fct to image
                img_corrupted = Image.fromarray(np.uint8(img_corrupted))

                # save corrupted image (overwrite downloaded clean image)
                img_corrupted.save(img_path)


if __name__ == "__main__":
    main()
