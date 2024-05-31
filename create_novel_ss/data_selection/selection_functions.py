# This software was created by Oregon State University under Army Research
# Office (ARO) Award Number W911NF-22-2-0149. ARO, as the Federal awarding
# agency, reserves a royalty-free, nonexclusive and irrevocable right to
# reproduce, publish, or otherwise use this software for Federal purposes, and
# to authorize others to do so in accordance with 2 CFR 200.315(b).

from config.config import ACT_THRESHOLDS, SPECIES, ENVIRONMENTS

def candidate_no_novelty(metadata):
    """
    Get capture_id of all images satisfying the no-novelty conditions
    """
    
    metadata_df = metadata.copy(deep=True)
            
    # candidate pre-novelty images are images taken during day time
    metadata_df = metadata_df.loc[metadata_df['moment_of_the_day'] == 'day']

    # exclude all sequence numbers that where species do not have meet the required known and novel concensus threshold
    seq_ids_known_act = metadata_df['capture_id'].loc[
        (
            (metadata_df['question__standing'] >= ACT_THRESHOLDS['known']) & 
            (metadata_df['question__moving'] < ACT_THRESHOLDS['novel'])
            ) | 
        (
            (metadata_df['question__standing'] < ACT_THRESHOLDS['novel']) & 
            (metadata_df['question__moving'] >= ACT_THRESHOLDS['known'])
            )
        ]
    metadata_df = metadata_df.loc[metadata_df['capture_id'].isin(seq_ids_known_act)].reset_index()

    # exclude all sequences with activity resting, eating or interacting (novel activities)
    seq_ids_novel_act = metadata_df['capture_id'].loc[
        (metadata_df['question__resting'] > ACT_THRESHOLDS['novel']) |
        (metadata_df['question__eating'] > ACT_THRESHOLDS['novel']) |
        (metadata_df['question__interacting'] > ACT_THRESHOLDS['novel']) |
        ((metadata_df['question__standing'] > ACT_THRESHOLDS['known']) & 
            (metadata_df['question__moving'] > ACT_THRESHOLDS['known'])
            )
    ]
    metadata_df = metadata_df.loc[~metadata_df['capture_id'].isin(seq_ids_novel_act)].reset_index()
        
    # exclude all capture event containing species not in the known species set
    seq_id_not_known_spe = metadata_df.loc[~metadata_df['question__species'].isin(SPECIES['known'])]['capture_id']
    metadata_df = metadata_df.loc[~metadata_df['capture_id'].isin(seq_id_not_known_spe)]

    # exclude images containing more than one species
    metadata_df = metadata_df.drop_duplicates('capture_id', keep=False)

    return metadata_df[['capture_id', 'question__species']]


def candidate_novel_species(metadata):
    """
    Get the sequence id of images satisfying the novel species conditions
    """
    metadata_df = metadata.copy(deep=True)
            
    # candidate pre-novelty images are images taken during day time
    metadata_df = metadata_df.loc[metadata_df['moment_of_the_day'] == 'day']

    # exclude all sequence numbers that where species do not have meet the required known and novel concensus threshold
    seq_ids_known_act = metadata_df['capture_id'].loc[
        (
            (metadata_df['question__standing'] >= ACT_THRESHOLDS['known']) & 
            (metadata_df['question__moving'] < ACT_THRESHOLDS['novel'])
            ) | 
        (
            (metadata_df['question__standing'] < ACT_THRESHOLDS['novel']) & 
            (metadata_df['question__moving'] >= ACT_THRESHOLDS['known'])
            )
        ]
    metadata_df = metadata_df.loc[metadata_df['capture_id'].isin(seq_ids_known_act)].reset_index()

    # exclude all sequences with activity resting, eating or interacting (novel activities)
    seq_ids_novel_act = metadata_df['capture_id'].loc[
        (metadata_df['question__resting'] > ACT_THRESHOLDS['novel']) |
        (metadata_df['question__eating'] > ACT_THRESHOLDS['novel']) |
        (metadata_df['question__interacting'] > ACT_THRESHOLDS['novel']) |
        (
            (metadata_df['question__standing'] > ACT_THRESHOLDS['known']) & 
            (metadata_df['question__moving'] > ACT_THRESHOLDS['known'])
        )
    ]
    metadata_df = metadata_df.loc[~metadata_df['capture_id'].isin(seq_ids_novel_act)].reset_index()

    # exclude all sequence id containing more than one known species
    metadata_df_known = metadata_df.loc[metadata_df['question__species'].isin(SPECIES['known'])]
    seq_id_more_than_1_known_spe = metadata_df_known[metadata_df_known.duplicated(keep=False)]['capture_id']
    metadata_df = metadata_df.loc[~metadata_df['capture_id'].isin(seq_id_more_than_1_known_spe)]

    # keep only images containing at least one novel species
    metadata_df = metadata_df.loc[metadata_df['question__species'].isin(SPECIES['novel'])]

    return metadata_df[['capture_id', 'question__species']]


def candidate_novel_activities(metadata):
    """
    Get the sequence id of images satisfying the novel activities conditions
    """
    metadata_df = metadata.copy(deep=True)

    # candidate novelty type 3 are images taken during day time like known prenovelty
    metadata_df = metadata_df.loc[metadata_df['moment_of_the_day'] == 'day']

    # exclude all capture event containing species not in the known species set
    seq_id_not_known_spe = metadata_df.loc[~metadata_df['question__species'].isin(SPECIES['known'])]['capture_id']
    metadata_df = metadata_df.loc[~metadata_df['capture_id'].isin(seq_id_not_known_spe)]

    # exclude all sequence id containing any novel species
    seq_id_novel_spe_imgs = metadata_df.loc[metadata_df['question__species'].isin(SPECIES['novel'])][
        'capture_id']
    metadata_df = metadata_df.loc[~metadata_df['capture_id'].isin(seq_id_novel_spe_imgs)].reset_index()

    # Exclude all sequence numbers that where species do not have meet the required known and novel concensus threshold
    seq_ids1 = metadata_df['capture_id'].loc[
        (
            (
                (metadata_df['question__standing'] >= ACT_THRESHOLDS['known']) & 
                (metadata_df['question__moving'] < ACT_THRESHOLDS['novel'])
                ) | 
            (
                (metadata_df['question__standing'] < ACT_THRESHOLDS['novel']) & 
                (metadata_df['question__moving'] >= ACT_THRESHOLDS['known'])
                )  | 
            (
                (metadata_df['question__standing'] < ACT_THRESHOLDS['novel']) & 
                (metadata_df['question__moving'] < ACT_THRESHOLDS['novel'])
                )
        ) &
        (
            (metadata_df['question__eating'] >= ACT_THRESHOLDS['known']) | 
            (metadata_df['question__resting'] >= ACT_THRESHOLDS['known'])
        )
        ]
    metadata_df = metadata_df.loc[metadata_df['capture_id'].isin(seq_ids1)].reset_index()

    # exclude all images containing more than one species
    metadata_df = metadata_df.drop_duplicates('capture_id', keep=False)

    return metadata_df[['capture_id', 'question__species']]


def candidate_comb_species(metadata):
    """
    Get the sequence id of images satisfying the novel combination of species conditions
    """
    metadata_df = metadata.copy(deep=True)

    # candidate novelty type 4 are images taken during day time like known prenovelty
    metadata_df = metadata_df.loc[metadata_df['moment_of_the_day'] == 'day']

    # exclude all capture event containing species not in the known species set
    seq_id_not_known_spe = metadata_df.loc[~metadata_df['question__species'].isin(SPECIES['known'])]['capture_id']
    metadata_df = metadata_df.loc[~metadata_df['capture_id'].isin(seq_id_not_known_spe)]

    # exclude all images containing only one species (not having duplicate sequence ID)
    metadata_df = metadata_df[metadata_df.duplicated('capture_id', keep=False)]

    # exclude all sequence numbers that where species do not have meet the required known and novel concensus threshold
    seq_ids_known_act = metadata_df['capture_id'].loc[
        (
            (metadata_df['question__standing'] >= ACT_THRESHOLDS['known']) & 
            (metadata_df['question__moving'] < ACT_THRESHOLDS['novel'])
            ) | 
        (
            (metadata_df['question__standing'] < ACT_THRESHOLDS['novel']) & 
            (metadata_df['question__moving'] >= ACT_THRESHOLDS['known'])
            )
        ]
    metadata_df = metadata_df.loc[metadata_df['capture_id'].isin(seq_ids_known_act)].reset_index()

    # exclude all sequences with activity resting, eating or interacting (novel activities)
    seq_ids_novel_act = metadata_df['capture_id'].loc[
        (metadata_df['question__resting'] > ACT_THRESHOLDS['novel']) |
        (metadata_df['question__eating'] > ACT_THRESHOLDS['novel']) |
        (metadata_df['question__interacting'] > ACT_THRESHOLDS['novel']) |
        (
            (metadata_df['question__standing'] > ACT_THRESHOLDS['known']) & 
            (metadata_df['question__moving'] > ACT_THRESHOLDS['known'])
        )
    ]
    metadata_df = metadata_df.loc[~metadata_df['capture_id'].isin(seq_ids_novel_act)].reset_index()

    # return metadata_df['capture_id'].unique()
    return metadata_df[['capture_id']].drop_duplicates('capture_id', keep='first')


def candidate_comb_activities(metadata):
    """
    Get the sequence id of images satisfying the novel combination of activities conditions
    (There are only two known activities, so both will be present)
    """
    metadata_df = metadata.copy(deep=True)

    # candidate novelty type 5 are images taken during day time like known prenovelty
    metadata_df = metadata_df.loc[metadata_df['moment_of_the_day'] == 'day']

    # exclude all capture event containing species not in the known species set
    seq_id_not_known_spe = metadata_df.loc[~metadata_df['question__species'].isin(SPECIES['known'])]['capture_id']
    metadata_df = metadata_df.loc[~metadata_df['capture_id'].isin(seq_id_not_known_spe)]

    # exclude all images containing more than one species
    metadata_df = metadata_df.drop_duplicates('capture_id', keep=False)

    # select only images containing both known activities and no novel activity
    seq_ids = metadata_df['capture_id'].loc[
        (
            (metadata_df['question__standing'] >= ACT_THRESHOLDS['known-comb_act']) & 
            (metadata_df['question__moving'] >= ACT_THRESHOLDS['known-comb_act'])
        ) & 
        (
            (metadata_df['question__eating'] < ACT_THRESHOLDS['novel-comb_act']) & 
            (metadata_df['question__resting'] < ACT_THRESHOLDS['novel-comb_act'])
        )
        ]
    metadata_df = metadata_df.loc[metadata_df['capture_id'].isin(seq_ids)].reset_index()

    return metadata_df[['capture_id', 'question__species']]


def candidate_novel_env(metadata):
    """
    Get the sequence id of images satisfying the novel environment conditions
    """
    metadata_df = metadata.copy(deep=True)

    # exclude all capture event containing species not in the known species set
    seq_id_not_known_spe = metadata_df.loc[~metadata_df['question__species'].isin(SPECIES['known'])]['capture_id']
    metadata_df = metadata_df.loc[~metadata_df['capture_id'].isin(seq_id_not_known_spe)]

    # # exclude all images containing any novel species
    # seq_id_novel_spe_imgs = metadata_df.loc[metadata_df['question__species'].isin(SPECIES['novel'])]['capture_id']
    # metadata_df = metadata_df.loc[~metadata_df['capture_id'].isin(seq_id_novel_spe_imgs)].reset_index()

    # exclude all sequence numbers that where species do not have meet the required known and novel concensus threshold
    seq_ids_known_act = metadata_df['capture_id'].loc[
        (
            (metadata_df['question__standing'] >= ACT_THRESHOLDS['known']) & 
            (metadata_df['question__moving'] < ACT_THRESHOLDS['novel'])
            ) | 
        (
            (metadata_df['question__standing'] < ACT_THRESHOLDS['novel']) & 
            (metadata_df['question__moving'] >= ACT_THRESHOLDS['known'])
            )
        ]
    metadata_df = metadata_df.loc[metadata_df['capture_id'].isin(seq_ids_known_act)].reset_index()

    # exclude all sequences with activity resting, eating or interacting (novel activities)
    seq_ids_novel_act = metadata_df['capture_id'].loc[
        (metadata_df['question__resting'] > ACT_THRESHOLDS['novel']) |
        (metadata_df['question__eating'] > ACT_THRESHOLDS['novel']) |
        (metadata_df['question__interacting'] > ACT_THRESHOLDS['novel']) |
        (
            (metadata_df['question__standing'] > ACT_THRESHOLDS['known']) & 
            (metadata_df['question__moving'] > ACT_THRESHOLDS['known'])
        )
    ]
    metadata_df = metadata_df.loc[~metadata_df['capture_id'].isin(seq_ids_novel_act)].reset_index()

    # exclude all images containing more than one species (duplicate sequence ID)
    metadata_df = metadata_df.drop_duplicates('capture_id', keep=False)

    # images of known species only taken during novel lighting conditions
    metadata_df = metadata_df.loc[metadata_df['moment_of_the_day'].isin(ENVIRONMENTS['novel'])].copy(deep=True)

    # add sub-novelty time-of-day to the output dataframe
    metadata_df = metadata_df[['capture_id', 'question__species', 'moment_of_the_day']]
    metadata_df.rename(columns={'moment_of_the_day': 'sub_novelty_class'}, inplace=True)
    metadata_df['sub_novelty'] = 'moment_of_the_day'

    return metadata_df
