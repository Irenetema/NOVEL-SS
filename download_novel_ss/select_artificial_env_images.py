"""
Select a small subset of the training set that will be corrupted to create artificial novel environments
such as snow and fog
"""

import os
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm

from utils.corruptions import *

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



if __name__ == "__main__":
    N = 4000
    dir_imgs = '../../../../sail_on3/Images/prenovelty/'
    output_dir = '../../../../sail_on3/final/osu_train_cal_val/corrupted_train_images/'

    path_train = '../../../../sail_on3/final/train.csv'
    path_test = '../../../../sail_on3/final/test.csv'

    train_labels = pd.read_csv(path_train)
    test_labels = pd.read_csv(path_test, low_memory=False)

    corrupt_test = test_labels.loc[test_labels["environment_id"].isin([3, 4]), :]
    corrupt_test["image_path"] = corrupt_test["image_path"].apply(lambda x: x[:-5]+x[-4:])
    corrupt_test["filename"] = corrupt_test["filename"].apply(lambda x: x[:-5]+x[-4:])

    idx_train_in_test = train_labels["filename"].loc[train_labels["filename"].isin(list(corrupt_test["filename"]))]

    # train_not_in_test = train_labels.iloc[~idx_train_in_test, :]
    train_not_in_test = train_labels.drop(index=idx_train_in_test)
    


    type_of_corruptions = ('fog', 'snow')
    corruption_id = {
        'fog': 3, 
        'snow': 4
        }

    corr_severity = 1
    overwrite_existing = False

    all_train_corr = train_not_in_test.sample(n=N, replace=False)

    #images_per_corruption = {}
    for j, corr in enumerate(type_of_corruptions):

        if j == 0:
            train_corr = all_train_corr.head(int(N/2))
        elif j == 1:
            train_corr = all_train_corr.tail(int(N/2))
        else:
            raise ValueError("\n\n \#\# Only two corruptions implemented!\n")

        print(f'>> Starting corruption of corruption type: {corr}')

        list_imgs_corr = train_corr['filename'].to_list() 

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        elif not overwrite_existing:
            # get the name of all the files already processed
            list_f_in_dir = os.listdir(output_dir)
            list_imgs_corr = list(set(list_imgs_corr) - set(list_f_in_dir))

        if corr == 'fog':
            corr_severity = 2
            # continue

        for img_fname in tqdm(list_imgs_corr):
            image = Image.open(dir_imgs+img_fname)
            try:
                img_corrupted = corrupt(image, severity=corr_severity, corruption_name=corr, corruption_number=-1)
            except Exception as ex:
                print(f'The following exception happened: {ex}')
                continue

            # convert the np array returned by "corrupt" fct to image
            img_corrupted = Image.fromarray(np.uint8(img_corrupted))

            ## save corrupted image
            # img_corrupted.save(output_dir+'/'+img_fname[:-4]+f'_{corr}'+img_fname[-4:])
            img_corrupted.save(output_dir+'/'+img_fname)
        

        train_corr["novelty_type"] = 6
        train_corr["environment_id"] = corruption_id[corr]
        # train_corr["filename"] = train_corr["filename"].apply(lambda x: x[:-4]+f'_{corr}'+x[-4:])
        train_corr["image_path"] = train_corr["filename"].apply(lambda x: 'final/osu_train_cal_val/corrupted_train_images/'+x)
        train_corr.to_csv('/'.join(output_dir.split('/')[:-2]) + f'/train_corrupt_{corr}.csv')
