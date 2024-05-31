# This software was created by Oregon State University under Army Research
# Office (ARO) Award Number W911NF-22-2-0149. ARO, as the Federal awarding
# agency, reserves a royalty-free, nonexclusive and irrevocable right to
# reproduce, publish, or otherwise use this software for Federal purposes, and
# to authorize others to do so in accordance with 2 CFR 200.315(b).

# pip3 install astral   # python package for calculating the time of various aspects of the sun and phases of the moon
import os
import argparse
import pandas as pd
from copy import deepcopy
from pathlib import Path
import tqdm

from astral import LocationInfo

from create_novel_ss.data_selection.utils import partition_capture_time
from config.config import NOVELTY_TYPES
from create_novel_ss.data_selection.selection_functions import *


# Serengeti national park geo-location information for daily extracting sunrise and sunset time
SerengetiPark = LocationInfo(
    name='Serengeti',
    region='Tanzania',
    timezone='Africa/Dar_es_Salaam',
    latitude=-2.333333,
    longitude=34.833332
)

def preprocess_metadata(meta_data):
    # discard blank and human classes
    p_metadata = deepcopy(meta_data.loc[~meta_data['question__species'].isin(['blank', 'human'])])

    # lower case the species name to reduce label (redundancy)
    p_metadata['question__species'] = p_metadata['question__species'].str.lower()

    # rename birdother as otherbird since the two labels refer to the same class
    p_metadata.loc[p_metadata['question__species'] == 'birdother', 'question__species'] = 'otherbird'

    # rename season 11 from SER_S11 to S11 for consistency
    p_metadata['season'] = p_metadata['season'].apply(lambda x: 'S11' if x == 'SER_S11' else x)

    # classify images per moment of the day (daytime, dusk, night time and dawn)
    p_metadata['capture_datetime_local'] = pd.to_datetime(
        p_metadata['capture_date_local'] + ' ' + p_metadata['capture_time_local']
    )
    p_metadata['moment_of_the_day'] = p_metadata['capture_datetime_local'].apply(
        partition_capture_time,
        city=SerengetiPark
    )

    return p_metadata


def get_image_labels_from_sequence_id(
        ss_sequence_metada, ss_image_metadata, 
        candidate_sequences, novelty_type='no_novelty'
    ):
    """
    Get the full image url from the sequence/capture ids
    Arguments:
        ss_sequence_metada (pd.DataFrame): snapshot Serengeti sequences annotations file
        ss_image_metada (pd.DataFrame): snapshot Serengeti images annotation file
        candidate_sequences (pd.DataFrame): sequence/capture ids of candidate images
    
    return: (pd.DataFrame) full label of images in candidate_sequences
    """

    assert novelty_type in NOVELTY_TYPES

    select_cols = [
        'capture_id', 'question__species', 'question__count_median', 'question__count_max', 'question__standing',
        'question__moving', 'question__resting', 'question__eating', 'question__interacting'
    ]

    if novelty_type == 'novel_environment':
        select_cols += ['capture_time_local', 'capture_date_local']

    # print(f'novetly columns: {novelty_all_candidates.columns}')
    seq_ids = candidate_sequences['capture_id']

    imgs_path = ss_image_metadata[['capture_id', 'image_path_rel']].loc[
        ss_image_metadata['capture_id'].isin(seq_ids)
    ]
    all_metadata = ss_sequence_metada.loc[ss_sequence_metada['capture_id'].isin(seq_ids)]

    images_ids = pd.merge(imgs_path, all_metadata[select_cols], on='capture_id', how='right')

    return images_ids


def main():
    parser = argparse.ArgumentParser(
        description='Select images from the SS labels that match the definition of each novelty type'
    )
    parser.add_argument(
        '--path_ss_annotations',
        default='PATH_TO_SS_LABELS/SnapshotSerengeti_v2_1_annotations_all.csv',
        help='Path to SS dataset annotations csv file (sequence level annotations)'
    )
    parser.add_argument(
        '--path_ss_images_url',
        default='PATH_TO_SS_LABELS/SnapshotSerengeti_v2_1_images_all.csv',
        help='Path to csv file containing the url of images in the annotations sequence'
    )
    parser.add_argument(
        '--output_dir',
        help='Directory for output images (defaults to same as input)'
    )

    args = parser.parse_args()

    assert os.path.exists(args.path_ss_annotations), '* SS annotation file {} does not exist!'.format(args.path_ss_annotations)
    assert os.path.exists(args.path_ss_images_url), '* SS images url file {} does not exist!'.format(args.path_ss_images_url)
    assert os.path.exists(args.output_dir), '* Output directory {} does not exist!'.format(args.output_dir)

    # Load SS sequences annotation file and images url file
    df_seq_annotation = pd.read_csv(args.path_ss_annotations, index_col=[0], low_memory=False)
    df_images_annotation = pd.read_csv(args.path_ss_images_url, index_col=[0])

    df_seq_annotation = preprocess_metadata(df_seq_annotation)

    print(f'\n** Selecting candidate sequences of images...\n')

    no_novelty_seq = candidate_no_novelty(df_seq_annotation)
    # print('>> no novelty candidate image sequences selection complete..')

    novel_spe_seq = candidate_novel_species(df_seq_annotation)
    # print('>> novel species candidate image sequences selection complete..')

    novel_act_seq = candidate_novel_activities(df_seq_annotation)
    # print('>> novel activities candidate image sequences selection complete..')

    novel_comb_spe_seq = candidate_comb_species(df_seq_annotation)
    # print('>> novel combination of species candidate image sequences selection complete..')

    novel_comb_act_seq = candidate_comb_activities(df_seq_annotation)
    # print('>> novel combination of activities candidate image sequences selection complete..')

    novel_env_seq = candidate_novel_env(df_seq_annotation)
    # print('>> novel environment candidate image sequences selection complete..')

    all_seq_ids = [
        no_novelty_seq, novel_spe_seq, novel_act_seq, 
        novel_comb_spe_seq, novel_comb_act_seq, novel_env_seq
    ]
    

    print(f'\n\n** Getting image labels of candidate sequences...\n')

    # get the url of images whose sequence_id (capture_id) was selected as candidate
    for novelty_type, seq_ids in zip(NOVELTY_TYPES, all_seq_ids):
        image_labels = get_image_labels_from_sequence_id(
            df_seq_annotation, 
            df_images_annotation, 
            seq_ids, novelty_type
        )

        # *** save labels
        assert os.path.exists(args.output_dir)

        labels_dir = args.output_dir + 'label_candidates/'

        # create labels_dir if it does not exist and save image labels for novelty type
        Path(labels_dir).mkdir(parents=True, exist_ok=True)
        image_labels.to_csv(
            os.path.join(labels_dir, f'{novelty_type}_labels.csv')
        )

        
    print('** candidate image selection complete!')
    print(f'\n>> candidate image labels saved in: {labels_dir}')
    


if __name__ == '__main__':
    main()
