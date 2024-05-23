from doctest import master
import os
import pandas as pd
import numpy as np
import random
from copy import deepcopy
from tqdm import tqdm
import json

from json_utils import NanConverter

np.random.seed(10000)

'''
columns_to_take = [
    'image_path', 'filename', 'capture_id', 'width', 'height', 'agent1_name', 'agent1_id', 'agent1_count', 
    'agent2_name', 'agent2_id', 'agent2_count', 'agent3_name', 'agent3_id', 'agent3_count', 'activities',
    'activities_id', 'environment', 'environment_id', 'novelty_type', 'master_id']
'''

columns_to_take = [
    'image_path', 'filename', 'capture_id', 'width', 'height', 'agent1_name', 'agent1_id', 'agent1_count', 
    'agent2_name', 'agent2_id', 'agent2_count', 'agent3_name', 'agent3_id', 'agent3_count', 'activities',
    'activities_id', 'environment_id', 'novelty_type', 'master_id']


all_known_species = (
        'blank', 'zebra', 'gazellethomsons', 'wildebeest', 'elephant', 'gazellegrants', 
        'otherbird', 'topi', 'giraffe', 'lionfemale', 'hyenaspotted'
)

all_novel_species = (
    'impala', 'buffalo', 'hippopotamus', 'guineafowl', 'hartebeest', 'warthog', 'mongoose', 'baboon', 
    'dikdik', 'cheetah', 'koribustard', 'insectspider', 'jackal', 'ostrich', 'reedbuck', 'eland'
)

novelty_types = ('type2', 'type3', 'type4', 'type5', 'type6')

# keys_to_take = ('image_path', 'capture_id', 'height', 'width', 'agent_count', 'agent_id', 'agent_name', 'bboxes')
keys_to_take = ('image_path', 'capture_id', 'height', 'width', 'bboxes')

# distribtuion of known species in the prenovelty test set
dist_known_species = {
    'blank':0.058, 
    'zebra':0.21, 
    'gazellethomsons':0.30, 
    'wildebeest':0.18, 
    'elephant':0.06, 
    'gazellegrants':0.05, 
    'otherbird':0.03, 
    'topi':0.015, 
    'giraffe':0.07, 
    'lionfemale':0.01, 
    'hyenaspotted':0.017
}

# novel species to leave out for validatation (remaining used for testing)
type2_val = ('koribustard', 'eland')  

# activity and species used for type 3 novelty validation set
type3_val = {
    'eating': ('wildebeest', 'topi'),
    'resting': None
    }
# type4_val = ('zebra', 'wildebeest', 'gazellethomsons', 'giraffe', 'otherbird')
type4_val = [
    set(('zebra', 'gazellethomsons')), set(('giraffe', 'zebra')), 
    set(('wildebeest', 'otherbird')), set(('otherbird', 'gazellethomsons'))
    ]

type5_val = ('elephant', 'wildebeest', 'topi')

# species and environment used for type 6 novelty validation set
type6_val = {
    'species': ('zebra', 'wildebeest'),
    'moment': (0, 1, 3, 4), # 0=day, 1=dawn/dusk and 2=night
    }  # images taken at day time are images with artificial noise (fog and snow)

novelty_val = {
    'type2': type2_val,
    'type3': type3_val,
    'type4': type4_val,
    'type5': type5_val,
    'type6': type6_val
}


dump_path = ''
trial_size = 1000


def integer(x):
    if x is None:
        return x
    return int(x)


def train_val_test_split(path_final_csv_json_dir, path_output_dir, size_prenovelty_test=10000):
    """
    Divide the finally processed json files (for each novlety type) into train, validation and test sets.
    The training set is made of prenovelty images only. While the validation set will contain only novel
    images since the teams could just leave a subset of training out for prenovelty validation.
    Arguments:
        path_final_csv_json_dir: path to directory containing the final csv and json files for each novelty type
        path_output_dir: path to directory in which the final train, valid and test file are to be saved
        size_prenovelty_tests: number of images from prenovelty to leave out for test set
    """
    global novelty_val, novelty_types, all_known_species, all_novel_species, dist_known_species
    np.random.seed(100000)

    assert os.path.exists(os.path.join(path_final_csv_json_dir, 'prenovelty.json'))
    for novelty in novelty_types:
        assert os.path.exists(path_final_csv_json_dir+f'{novelty}_novelty.json')

    f1 = open(os.path.join(path_final_csv_json_dir, 'prenovelty.json'))
    prenovelty_dict = json.load(f1)

    f2 = open(os.path.join(path_final_csv_json_dir, 'type2_novelty.json'))
    type2_novelty_dict = json.load(f2)

    f3 = open(os.path.join(path_final_csv_json_dir, 'type3_novelty.json'))
    type3_novelty_dict = json.load(f3)

    f4 = open(os.path.join(path_final_csv_json_dir, 'type4_novelty.json'))
    type4_novelty_dict = json.load(f4)

    f5 = open(os.path.join(path_final_csv_json_dir, 'type5_novelty.json'))
    type5_novelty_dict = json.load(f5)

    f6 = open(os.path.join(path_final_csv_json_dir, 'type6_novelty.json'))
    type6_novelty_dict = json.load(f6)

    
    prenovelty_df = pd.read_csv(os.path.join(path_final_csv_json_dir, 'prenovelty.csv'))
    if True:
        print('\n\n', '*'*100)
        print(' >>>>>> Changing environment and environment_id for prenovelty! Change it if not modified from type 6 for testing.')
        print('', '*'*100, '\n\n')
        prenovelty_df['environment'] = 'day'
        prenovelty_df['environment_id'] = 0

    type2_novelty_df = pd.read_csv(os.path.join(path_final_csv_json_dir, 'type2_novelty.csv'))
    type3_novelty_df = pd.read_csv(os.path.join(path_final_csv_json_dir, 'type3_novelty.csv'))
    type4_novelty_df = pd.read_csv(os.path.join(path_final_csv_json_dir, 'type4_novelty.csv'))
    type5_novelty_df = pd.read_csv(os.path.join(path_final_csv_json_dir, 'type5_novelty.csv'))
    type6_novelty_df = pd.read_csv(os.path.join(path_final_csv_json_dir, 'type6_novelty.csv'))

    # train_set, val_set, test_set = {}, {}, {}
    master_info = {}  # information about images needed to provide feedback when requested

    if os.path.exists(os.path.join(path_final_csv_json_dir, 'blank.csv')):
        # join prenovelty and blank images (blank is one class of prenovelty)
        blank_df = pd.read_csv(os.path.join(path_final_csv_json_dir, 'blank.csv'))
        prenovelty_df = pd.concat([blank_df, prenovelty_df])

        f0 = open(os.path.join(path_final_csv_json_dir, 'blank.json'))
        blank_dict = json.load(f0)
        prenovelty_dict = {**blank_dict, **prenovelty_dict} 

    assert os.path.exists('name2id_dictionaries/environment_id_mapping.json')

    # {"0": "day", "1": "dawn-dusk", "2": "night", "3": "day-fog", "4": "day-snow"}
    f_e = open('name2id_dictionaries/environment_id_mapping.json')
    environment_id_dict = json.load(f_e)

    # {"activity_standing": 0, "activity_moving": 1, "activity_resting": 2, "activity_eating": 3, "activity_interacting": 4}
    f_a = open('name2id_dictionaries/activity_id_mapping.json')
    activity2id_dict = json.load(f_a)

    def get_env_id(moment, noise):
        if int(moment) == 0 and  int(noise) == 0:
            # day time and no artificial corruption
            # return 0
            return list(environment_id_dict.keys())[list(environment_id_dict.values()).index('day')]
        elif int(moment) == 1 and  int(noise) == 0:
            # dawn/dusk time and no artificial corruption
            # return 1
            return list(environment_id_dict.keys())[list(environment_id_dict.values()).index('dawn-dusk')]
        elif int(moment) == 2 and  int(noise) == 0:
            # night time and no artificial corruption
            # return 2
            return list(environment_id_dict.keys())[list(environment_id_dict.values()).index('night')]
        elif int(moment) == 0 and  int(noise) == 1:
            # day time and fog artificial corruption
            # return 3
            return list(environment_id_dict.keys())[list(environment_id_dict.values()).index('day-fog')]
        elif int(moment) == 0 and  int(noise) == 2:
            # day time and snow artificial corruption
            # return 4
            return list(environment_id_dict.keys())[list(environment_id_dict.values()).index('day-snow')]
        else:
            raise ValueError('moment and noise argument not correct in "get_env_id"!')


    # ****************************************
    # ******** Test set creation *************
    # ****************************************

    # -----------------------------------------------------------
    # ////////////// Prenovelty train and test set //////////////
    # -----------------------------------------------------------

    nbr_img_per_class = {x: int(dist_known_species[x]*size_prenovelty_test) for x in dist_known_species.keys()}
   
    list_selected_imgs = []
    for species in dist_known_species.keys():
        # get images of species
        species_df = prenovelty_df[['capture_id', 'filename', 'agent1_name']].loc[prenovelty_df['agent1_name']==species]
        
        assert len(species_df) > 0

        # shuffle the capture_ids for randomly selecting images
        ids = species_df['capture_id'].unique()
        random.shuffle(ids)
        species_df = species_df.set_index('capture_id').loc[ids].reset_index()

        list_selected_imgs = list_selected_imgs + species_df['filename'].head(nbr_img_per_class[species]).tolist()
    
    test_set_bboxes = {}
    all_pnovelty_imgs = list(prenovelty_dict.keys())
    size_master = len(master_info.keys())
    for idx, img in enumerate(all_pnovelty_imgs):
        # get master information for feedback retrieval when requested
        agent1_name = prenovelty_df.loc[prenovelty_df['filename']==img, 'agent1_name']
        master_info[idx+size_master] = {
            'filename': img,
            'agent1_id': prenovelty_df.loc[prenovelty_df['filename']==img, 'agent1_id'].item(),
            'agent1_name': prenovelty_df.loc[prenovelty_df['filename']==img, 'agent1_name'].values[0],
            'agent1_count': prenovelty_df.loc[prenovelty_df['filename']==img, 'agent1_count'].item(),
            'agent2_id': prenovelty_df.loc[prenovelty_df['filename']==img, 'agent2_id'].item(),
            'agent2_name': prenovelty_df.loc[prenovelty_df['filename']==img, 'agent2_name'].values[0],
            'agent2_count': prenovelty_df.loc[prenovelty_df['filename']==img, 'agent2_count'].item(),
            'agent3_id': prenovelty_df.loc[prenovelty_df['filename']==img, 'agent3_id'].item(),
            'agent3_name': prenovelty_df.loc[prenovelty_df['filename']==img, 'agent3_name'].values[0],
            'agent3_count': prenovelty_df.loc[prenovelty_df['filename']==img, 'agent3_count'].item(),
            'is_novel': 0,
            'novelty_type': 0,
            'activities': prenovelty_df.loc[prenovelty_df['filename']==img, 'activities'].values[0],
            'activities_id': prenovelty_df.loc[prenovelty_df['filename']==img, 'activities_id'].values[0],
            'environment': prenovelty_df.loc[prenovelty_df['filename']==img, 'environment'].values[0],
            'environment_id': prenovelty_df.loc[prenovelty_df['filename']==img, 'environment_id'].item()
            }


        if img in list_selected_imgs:
            # Test image
            test_set_bboxes[img] = prenovelty_dict[img]
            del prenovelty_dict[img]

            # prenovelty_df['image_path'].loc[prenovelty_df['filename']==img] = 'final/dataset/test/' + img
            prenovelty_df.loc[prenovelty_df['filename']==img, 'image_path'] = 'final/dataset/test/' + img
           
        else:
            # Training image: add image path to the dictionary
            # prenovelty_df['image_path'].loc[prenovelty_df['filename']==img] = 'final/dataset/train/' + img
            prenovelty_df.loc[prenovelty_df['filename']==img, 'image_path'] = 'final/dataset/train/' + img
            
        prenovelty_df.loc[prenovelty_df['filename']==img, 'master_id'] = idx+size_master       

        # delete blank images (no bounding boxes) from the dictionary
        if master_info[idx+size_master]['agent1_name'] == 'blank' and img in prenovelty_dict.keys():
            del prenovelty_dict[img]
    
    # the prenovelty images used for testing have all being removed from prenovelty_dict at this point
    train_set_bboxes = prenovelty_dict  

    prenovelty_test_set = deepcopy(prenovelty_df.loc[prenovelty_df['filename'].isin(list_selected_imgs)])
    prenovelty_test_set['novelty_type'] = 0
    prenovelty_df = prenovelty_df.loc[~prenovelty_df['filename'].isin(list_selected_imgs)]
    prenovelty_df['novelty_type'] = 0

    print(f'\n** length prenovelty test set: {len(prenovelty_test_set)}')
    print(f'** length prenovelty train set: {len(prenovelty_df)}')

    # -------------------------------------------------
    # //////////// Type 2 novelty test set //////////// 
    # -------------------------------------------------
    
    type2_val_species = novelty_val['type2']

    # type 2 novelty test species is the union of known species and species not in validation set
    type2_test_species = set(all_known_species) | (set(all_novel_species) - set(type2_val_species))

    type2_test_imgs = type2_novelty_df['filename'].loc[
        (type2_novelty_df['agent1_name'].isin(type2_test_species) == True) &
        (
            (type2_novelty_df['agent2_name'].isin(type2_test_species) == True) |
            (pd.isnull(type2_novelty_df.loc[:, 'agent2_name']))
        ) &
        (
            (type2_novelty_df['agent3_name'].isin(type2_test_species) == True) |
            (pd.isnull(type2_novelty_df.loc[:, 'agent2_name']))
        )
        ]

    # type2_novelty_test = {}
    all_novelty2_imgs = list(type2_novelty_dict.keys())
    size_master = len(master_info.keys())
    for idx, img in enumerate(all_novelty2_imgs):

        # get master information for feedback retrieval when requested
        master_info[idx+size_master] = {
            'filename': img,
            'agent1_id': type2_novelty_df.loc[type2_novelty_df['filename']==img, 'agent1_id'].item(),
            'agent1_name': type2_novelty_df.loc[type2_novelty_df['filename']==img, 'agent1_name'].values[0],
            'agent1_count': type2_novelty_df.loc[type2_novelty_df['filename']==img, 'agent1_count'].item(),
            'agent2_id': type2_novelty_df.loc[type2_novelty_df['filename']==img, 'agent2_id'].item(),
            'agent2_name': type2_novelty_df.loc[type2_novelty_df['filename']==img, 'agent2_name'].values[0],
            'agent2_count': type2_novelty_df.loc[type2_novelty_df['filename']==img, 'agent2_count'].item(),
            'agent3_id': type2_novelty_df.loc[type2_novelty_df['filename']==img, 'agent3_id'].item(),
            'agent3_name': type2_novelty_df.loc[type2_novelty_df['filename']==img, 'agent3_name'].values[0],
            'agent3_count': type2_novelty_df.loc[type2_novelty_df['filename']==img, 'agent3_count'].item(),
            'is_novel': 1,
            'novelty_type': 2,
            'activities': type2_novelty_df.loc[type2_novelty_df['filename']==img, 'activities'].values[0],
            'activities_ids': type2_novelty_df.loc[type2_novelty_df['filename']==img, 'activities_id'].values[0],
            'environment': type2_novelty_df.loc[type2_novelty_df['filename']==img, 'environment'].values[0],
            'environment_id': type2_novelty_df.loc[type2_novelty_df['filename']==img, 'environment_id'].item()
            }

        if img in type2_test_imgs:
            test_set_bboxes[img] = type2_novelty_dict[img]

            # delete selected image from type2 novelty dict (remaining images will be type 2 test set)
            del type2_novelty_dict[img]

            # type2_novelty_df['image_path'].loc[type2_novelty_df['filename']==img] = 'final/dataset/test/' + img
            type2_novelty_df.loc[type2_novelty_df['filename']==img, 'image_path'] = 'final/dataset/test/' + img
        else:
            # validation image: add image path to type 2 novelty dictionary
            type2_novelty_df.loc[type2_novelty_df['filename']==img, 'image_path'] = 'final/dataset/valid/' + img

        type2_novelty_df.loc[type2_novelty_df['filename']==img, 'master_id'] = idx+size_master

    # the type 2 novelty images used for testing have all being removed from type2_novelty_dict at this point
    valid_set_bboxes = type2_novelty_dict

    type2_novelty_df['novelty_type'] = 2
    type2_novelty_test_set = deepcopy(type2_novelty_df.loc[type2_novelty_df['filename'].isin(type2_test_imgs)])
    type2_novelty_df = type2_novelty_df.loc[~type2_novelty_df['filename'].isin(type2_test_imgs)]
    test_set_df = pd.concat([prenovelty_test_set, type2_novelty_test_set], ignore_index=True)

    print(f'\n** length type 2 test set: {len(type2_novelty_test_set)}')
    print(f'** length type 2 valid set: {len(type2_novelty_df)}')


    # -------------------------------------------------
    # //////////// Type 3 novelty test set //////////// 
    # -------------------------------------------------
    
    type3_val_species = novelty_val['type3']
    type3_test_imgs = type3_novelty_df['filename'].loc[
        ~(
            type3_novelty_df['agent1_name'].isin(type3_val_species['eating']) &
            (type3_novelty_df['activity_eating'] == 1) & 
            (type3_novelty_df['activity_resting'] == 0)
        )
        ]

    # type3_novelty_test = {}
    all_novelty3_imgs = list(type3_novelty_dict.keys())
    size_master = len(master_info.keys())
    for idx, img in enumerate(all_novelty3_imgs):

        # get master information for feedback retrieval when requested
        master_info[idx+size_master] = {
            'filename': img,
            'agent1_id': type3_novelty_df.loc[type3_novelty_df['filename']==img, 'agent1_id'].item(),
            'agent1_name': type3_novelty_df.loc[type3_novelty_df['filename']==img, 'agent1_name'].values[0],
            'agent1_count': type3_novelty_df.loc[type3_novelty_df['filename']==img, 'agent1_count'].item(),
            'agent2_id': type3_novelty_df.loc[type3_novelty_df['filename']==img, 'agent2_id'].item(),
            'agent2_name': type3_novelty_df.loc[type3_novelty_df['filename']==img, 'agent2_name'].values[0],
            'agent2_count': type3_novelty_df.loc[type3_novelty_df['filename']==img, 'agent2_count'].item(),
            'agent3_id': type3_novelty_df.loc[type3_novelty_df['filename']==img, 'agent3_id'].item(),
            'agent3_name': type3_novelty_df.loc[type3_novelty_df['filename']==img, 'agent3_name'].values[0],
            'agent3_count': type3_novelty_df.loc[type3_novelty_df['filename']==img, 'agent3_count'].item(),
            'is_novel': 1,
            'novelty_type': 3,
            'activities': type3_novelty_df.loc[type3_novelty_df['filename']==img, 'activities'].values[0],
            'activities_id': type3_novelty_df.loc[type3_novelty_df['filename']==img, 'activities_id'].values[0],
            # 'activity_ids': type3_novelty_df['activities_id'].loc[type3_novelty_df['filename']==img].values[0],
            'environment': type3_novelty_df.loc[type3_novelty_df['filename']==img, 'environment'].values[0],
            'environment_id': type3_novelty_df.loc[type3_novelty_df['filename']==img, 'environment_id'].item()
            }

        if img in type3_test_imgs:
            test_set_bboxes[img] = type3_novelty_dict[img]

            # delete selected image from type3 novelty dict (remaining images will be type 2 test set)
            del type3_novelty_dict[img]

            type3_novelty_df.loc[type3_novelty_df['filename']==img, 'image_path'] = 'final/dataset/test/' + img
        else:
            # validation image: add image path to type 3 novelty dictionary
            type3_novelty_df.loc[type3_novelty_df['filename']==img, 'image_path'] = 'final/dataset/valid/' + img

        type3_novelty_df.loc[type3_novelty_df['filename']==img, 'master_id'] = idx+size_master

    # the type 3 novelty images used for testing have all being removed from type3_novelty_dict at this point
    valid_set_bboxes = {**valid_set_bboxes, **type3_novelty_dict}

    type3_novelty_df['novelty_type'] = 3
    type3_novelty_test_set = deepcopy(type3_novelty_df.loc[type3_novelty_df['filename'].isin(type3_test_imgs)])
    type3_novelty_df = type3_novelty_df.loc[~type3_novelty_df['filename'].isin(type3_test_imgs)]
    test_set_df = pd.concat([test_set_df, type3_novelty_test_set], ignore_index=True)
    valid_set_df = pd.concat([type2_novelty_df, type3_novelty_df], ignore_index=True)

    print(f'\n** length type 3 test set: {len(type3_novelty_test_set)}')
    print(f'** length type 3 valid set: {len(type3_novelty_df)}')

    # -------------------------------------------------
    # //////////// Type 4 novelty test set //////////// 
    # -------------------------------------------------

    type4_val_duos = novelty_val['type4']

    type4_novelty_df['agents12_pair_in_val'] = type4_novelty_df[['agent1_name', 'agent2_name']].apply(
        lambda x: 1 if set([x['agent1_name'], x['agent2_name']]) in type4_val_duos else 0, axis=1
        )

    type4_test_imgs = type4_novelty_df['filename'].loc[
        ~(
            type4_novelty_df['agents12_pair_in_val'] == 1 &
            pd.isnull(type4_novelty_df['agent3_name'])
        )
        ]

    all_novelty4_imgs = list(type4_novelty_dict.keys())
    size_master = len(master_info.keys())
    for idx, img in enumerate(all_novelty4_imgs):

        # get master information for feedback retrieval when requested
        master_info[idx+size_master] = {
            'filename': img,
            'agent1_id': type4_novelty_df.loc[type4_novelty_df['filename']==img, 'agent1_id'].item(),
            'agent1_name': type4_novelty_df.loc[type4_novelty_df['filename']==img, 'agent1_name'].values[0],
            'agent1_count': type4_novelty_df.loc[type4_novelty_df['filename']==img, 'agent1_count'].item(),
            'agent2_id': type4_novelty_df.loc[type4_novelty_df['filename']==img, 'agent2_id'].item(),
            'agent2_name': type4_novelty_df.loc[type4_novelty_df['filename']==img, 'agent2_name'].values[0],
            'agent2_count': type4_novelty_df.loc[type4_novelty_df['filename']==img, 'agent2_count'].item(),
            'agent3_id': type4_novelty_df.loc[type4_novelty_df['filename']==img, 'agent3_id'].item(),
            'agent3_name': type4_novelty_df.loc[type4_novelty_df['filename']==img, 'agent3_name'].values[0],
            'agent3_count': type4_novelty_df.loc[type4_novelty_df['filename']==img, 'agent3_count'].item(),
            'is_novel': 1,
            'novelty_type': 4,
            'activities': type4_novelty_df.loc[type4_novelty_df['filename']==img, 'activities'].values[0],
            'activities_id': type4_novelty_df.loc[type4_novelty_df['filename']==img, 'activities_id'].values[0],
            'environment': type4_novelty_df.loc[type4_novelty_df['filename']==img, 'environment'].values[0],
            'environment_id': type4_novelty_df.loc[type4_novelty_df['filename']==img, 'environment_id'].item()
            }

        if img in type4_test_imgs:
            test_set_bboxes[img] = type4_novelty_dict[img]

            # delete selected image from type4 novelty dict (remaining images will be type 4 test set)
            del type4_novelty_dict[img]

            type4_novelty_df.loc[type4_novelty_df['filename']==img, 'image_path'] = 'final/dataset/test/' + img
        else:
            # validation image: add image path to type 4 novelty dictionary
            type4_novelty_df.loc[type4_novelty_df['filename']==img, 'image_path'] = 'final/dataset/valid/' + img

        type4_novelty_df.loc[type4_novelty_df['filename']==img, 'master_id'] = idx+size_master

    # the type 4 novelty images used for testing have all being removed from type4_novelty_dict at this point
    valid_set_bboxes = {**valid_set_bboxes, **type4_novelty_dict}

    type4_novelty_df['novelty_type'] = 4
    type4_novelty_test_set = deepcopy(type4_novelty_df.loc[type4_novelty_df['filename'].isin(type4_test_imgs)])
    type4_novelty_df = type4_novelty_df.loc[~type4_novelty_df['filename'].isin(type4_test_imgs)]
    test_set_df = pd.concat([test_set_df, type4_novelty_test_set], ignore_index=True)
    valid_set_df = pd.concat([valid_set_df, type4_novelty_df], ignore_index=True)

    print(f'\n** length type 4 test set: {len(type4_novelty_test_set)}')
    print(f'** length type 4 valid set: {len(type4_novelty_df)}')

    # -------------------------------------------------
    # //////////// Type 5 novelty test set //////////// 
    # -------------------------------------------------

    type5_val_species = novelty_val['type5']
    type5_test_imgs = type5_novelty_df['filename'].loc[
        ~(
            type5_novelty_df['agent1_name'].isin(type5_val_species)
        )
        ]

    all_novelty5_imgs = list(type5_novelty_dict.keys())
    size_master = len(master_info.keys())
    for idx, img in enumerate(all_novelty5_imgs):

        # get master information for feedback retrieval when requested
        master_info[idx+size_master] = {
            'filename': img,
            'agent1_id': type5_novelty_df.loc[type5_novelty_df['filename']==img, 'agent1_id'].item(),
            'agent1_name': type5_novelty_df.loc[type5_novelty_df['filename']==img, 'agent1_name'].values[0],
            'agent1_count': type5_novelty_df.loc[type5_novelty_df['filename']==img, 'agent1_count'].item(),
            'agent2_id': type5_novelty_df.loc[type5_novelty_df['filename']==img, 'agent2_id'].item(),
            'agent2_name': type5_novelty_df.loc[type5_novelty_df['filename']==img, 'agent2_name'].values[0],
            'agent2_count': type5_novelty_df.loc[type5_novelty_df['filename']==img, 'agent2_count'].item(),
            'agent3_id': type5_novelty_df.loc[type5_novelty_df['filename']==img, 'agent3_id'].item(),
            'agent3_name': type5_novelty_df.loc[type5_novelty_df['filename']==img, 'agent3_name'].values[0],
            'agent3_count': type5_novelty_df.loc[type5_novelty_df['filename']==img, 'agent3_count'].item(),
            'is_novel': 1,
            'novelty_type': 5,
            'activities': type5_novelty_df.loc[type5_novelty_df['filename']==img, 'activities'].values[0],
            'activities_id': type5_novelty_df.loc[type5_novelty_df['filename']==img, 'activities_id'].values[0],
            'environment': type5_novelty_df.loc[type5_novelty_df['filename']==img, 'environment'].values[0],
            'environment_id': type5_novelty_df.loc[type5_novelty_df['filename']==img, 'environment_id'].item()
            }

        if img in type5_test_imgs:
            test_set_bboxes[img] = type5_novelty_dict[img]

            # delete selected image from type5 novelty dict (remaining images will be type 5 test set)
            del type5_novelty_dict[img]

            type5_novelty_df.loc[type5_novelty_df['filename']==img, 'image_path'] = 'final/dataset/test/' + img
        else:
            # validation image: add image path to type 5 novelty dictionary
            type5_novelty_df.loc[type5_novelty_df['filename']==img, 'image_path'] = 'final/dataset/valid/' + img

        type5_novelty_df.loc[type5_novelty_df['filename']==img, 'master_id'] = idx+size_master

    # the type 5 novelty images used for testing have all being removed from type5_novelty_dict at this point
    valid_set_bboxes = {**valid_set_bboxes, **type5_novelty_dict}

    type5_novelty_df['novelty_type'] = 5
    type5_novelty_test_set = deepcopy(type5_novelty_df.loc[type5_novelty_df['filename'].isin(type5_test_imgs)])
    type5_novelty_df = type5_novelty_df.loc[~type5_novelty_df['filename'].isin(type5_test_imgs)]
    test_set_df = pd.concat([test_set_df, type5_novelty_test_set], ignore_index=True)
    valid_set_df = pd.concat([valid_set_df, type5_novelty_df], ignore_index=True)

    print(f'\n** length type 5 test set: {len(type5_novelty_test_set)}')
    print(f'** length type 5 valid set: {len(type5_novelty_df)}')

    # -------------------------------------------------
    # //////////// Type 6 novelty test set //////////// 
    # -------------------------------------------------

    type6_val = novelty_val['type6']

    # get images that do not satisfy the validation definition (dawn and dusk images of zebra and wildebeest and 
    # aritifial noise for those two species)
    type6_test_imgs = type6_novelty_df['filename'].loc[
        ~(
            (type6_novelty_df['agent1_name'].isin(type6_val['species'])) & 
            (type6_novelty_df['environment_id'].isin(type6_val['moment']))
            )
        ]

    all_novelty6_imgs = list(type6_novelty_dict.keys())
    size_master = len(master_info.keys())
    for idx, img in enumerate(all_novelty6_imgs):

        # get master information for feedback retrieval when requested
        master_info[idx+size_master] = {
            'filename': img,
            'agent1_id': type6_novelty_df.loc[type6_novelty_df['filename']==img, 'agent1_id'].item(),
            'agent1_name': type6_novelty_df.loc[type6_novelty_df['filename']==img, 'agent1_name'].values[0],
            'agent1_count': type6_novelty_df.loc[type6_novelty_df['filename']==img, 'agent1_count'].item(),
            'agent2_id': type6_novelty_df.loc[type6_novelty_df['filename']==img, 'agent2_id'].item(),
            'agent2_name': type6_novelty_df.loc[type6_novelty_df['filename']==img, 'agent2_name'].values[0],
            'agent2_count': type6_novelty_df.loc[type6_novelty_df['filename']==img, 'agent2_count'].item(),
            'agent3_id': type6_novelty_df.loc[type6_novelty_df['filename']==img, 'agent3_id'].item(),
            'agent3_name': type6_novelty_df.loc[type6_novelty_df['filename']==img, 'agent3_name'].values[0],
            'agent3_count': type6_novelty_df.loc[type6_novelty_df['filename']==img, 'agent3_count'].item(),
            'is_novel': 1,
            'novelty_type': 6,
            'activities': type6_novelty_df.loc[type6_novelty_df['filename']==img, 'activities'].values[0],
            'activities_id': type6_novelty_df.loc[type6_novelty_df['filename']==img, 'activities_id'].values[0],
            'environment': type6_novelty_df.loc[type6_novelty_df['filename']==img, 'environment'].values[0],
            'environment_id': type6_novelty_df.loc[type6_novelty_df['filename']==img, 'environment_id'].item()
            }

        if img in type6_test_imgs:
            test_set_bboxes[img] = type6_novelty_dict[img]

            # delete selected image from type6 novelty dict (remaining images will be type 6 test set)
            del type6_novelty_dict[img]

            type6_novelty_df.loc[type6_novelty_df['filename']==img, 'image_path'] = 'final/dataset/test/' + img
        else:
            # validation image: add image path to type 6 novelty dictionary
            type6_novelty_df.loc[type6_novelty_df['filename']==img, 'image_path'] = 'final/dataset/valid/' + img

        type6_novelty_df.loc[type6_novelty_df['filename']==img, 'master_id'] = idx+size_master

    # the type 6 novelty images used for testing have all being removed from type6_novelty_dict at this point
    valid_set_bboxes = {**valid_set_bboxes, **type6_novelty_dict}

    type6_novelty_df['novelty_type'] = 6
    type6_novelty_test_set = deepcopy(type6_novelty_df.loc[type6_novelty_df['filename'].isin(type6_test_imgs)])
    type6_novelty_df = type6_novelty_df.loc[~type6_novelty_df['filename'].isin(type6_test_imgs)]
    test_set_df = pd.concat([test_set_df, type6_novelty_test_set], ignore_index=True)
    valid_set_df = pd.concat([valid_set_df, type6_novelty_df], ignore_index=True)

    print(f'\n** length type 6 test set: {len(type6_novelty_test_set)}')
    print(f'** length type 6 valid set: {len(type6_novelty_df)}')


    # *************************************************
    # !!!!!!!!!!!! save csv and json files !!!!!!!!!!!! 
    #**************************************************

    # ----------  Save train, validation and testing csv files  ----------
    test_set_df[columns_to_take].to_csv(os.path.join(path_output_dir, 'test.csv'))
    prenovelty_df[columns_to_take].to_csv(os.path.join(path_output_dir, 'train.csv'))  # test set removed
    valid_set_df[columns_to_take].to_csv(os.path.join(path_output_dir, 'valid.csv'))

    # ----------  Save the bounding boxes in json files  ----------
    with open(path_output_dir+'master_ground_truth_info.json', 'w') as fp:
        json.dump(master_info, fp, cls=NanConverter)

    with open(path_output_dir+'train.json', 'w') as fp:
        json.dump(train_set_bboxes, fp)

    with open(path_output_dir+'valid.json', 'w') as fp:
        json.dump(valid_set_bboxes, fp)

    with open(path_output_dir+'test.json', 'w') as fp:
        json.dump(test_set_bboxes, fp)


if __name__ == '__main__':
    input_final_json_dir =  '/nfs/hpc/share/sail_on3/final/'
    output_final_json_dir =  '/nfs/hpc/share/sail_on3/final/'

    create_train_val_test = True
    
    train_val_test_split(
        path_final_csv_json_dir=input_final_json_dir+'final_novelty_labels/',
        path_output_dir=output_final_json_dir, 
        size_prenovelty_test=10000
    )

    