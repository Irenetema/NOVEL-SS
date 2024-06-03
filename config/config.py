# This software was created by Oregon State University under Army Research
# Office (ARO) Award Number W911NF-22-2-0149. ARO, as the Federal awarding
# agency, reserves a royalty-free, nonexclusive and irrevocable right to
# reproduce, publish, or otherwise use this software for Federal purposes, and
# to authorize others to do so in accordance with 2 CFR 200.315(b).

"""
Novelty types classes and hyper-parameters
"""

SS_URL = 'https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshotserengeti-unzipped/'

KNOWN_MONTHS = [i for i in range(1, 13)]
NOVEL_MONTHS = []

# Novelty types
NOVELTY_TYPES = [
    'no_novelty', 'novel_species', 'novel_activity',
    'novel_comb_species', 'novel_comb_activities', 
    'novel_environment'
]

# Known and novel activities selection
ACTIVITIES = {
    'known': ['standing', 'moving'],
    'novel': ['eating', 'resting']
}

# Known and novel species selection
SPECIES = {
    'known': [
        'zebra', 'gazellethomsons', 'wildebeest', 'elephant', 'gazellegrants', 
        'otherbird', 'topi', 'giraffe', 'lionfemale', 'hyenaspotted'
        ],
    'novel': [
        'impala', 'buffalo', 'hippopotamus', 'guineafowl', 'hartebeest', 
        'warthog', 'eland', 'baboon', 'reedbuck', 'dikdik', 'cheetah', 
        'mongoose', 'koribustard', 'insectspider', 'jackal', 'ostrich'
        ]
}

# Environments
ENVIRONMENTS = {
    'known': ['day'],
    'novel': ['dawn', 'dusk', 'dawn/dusk', 'night', 'fog', 'snow']
}

# Target proportion/frequency of known species in the final data
FREQ_KNOWN_SPECIES = {
    # 'blank': 0.05,
    'zebra': 0.22,
    'gazellethomsons': 0.3,
    'wildebeest': 0.3,
    'elephant': 0.03,
    'gazellegrants': 0.03,
    'otherbird': 0.02,
    'topi': 0.01,
    'giraffe': 0.02,
    'lionfemale': 0.01,
    'hyenaspotted': 0.01
}

# Target proportion/frequency of novel species in the final data
FREQ_NOVEL_SPECIES = {
    'impala': 0.17,
    'buffalo': 0.355,
    'hippopotamus': 0.015,
    'guineafowl': 0.133,
    'hartebeest': 0.133,
    'warthog': 0.081,
    'eland': 0.04,
    'baboon': 0.023,
    'reedbuck': 0.001,
    'dikdik': 0.005,
    'cheetah': 0.01,
    'mongoose': 0.005,
    'koribustard': 0.006,
    'insectspider': 0.014,
    'jackal': 0.002,
    'ostrich': 0.007
}

# Activities filtering thresholds
# ** Due to the small number of images in novel combination of activities,
# ** the threshold is loosen for that novelty type
ACT_THRESHOLDS = {
    'known': 0.95, 
    'novel': 0.05,
    'known-comb_act': 0.75,  
    'novel-comb_act': 0.25  # 0.15 
}

# Species ID to name map
SPECIES_ID2NAME = {
    "0": "wildebeest", 
    "1": "gazellegrants", 
    "2": "zebra", 
    "3": "elephant", 
    "4": "gazellethomsons", 
    "5": "giraffe", 
    "6": "otherbird", 
    "7": "lionfemale", 
    "8": "topi", 
    "9": "hyenaspotted", 
    "10": "buffalo", 
    "11": "impala", 
    "12": "dikdik", 
    "13": "warthog", 
    "14": "baboon", 
    "15": "guineafowl", 
    "16": "hartebeest", 
    "17": "koribustard", 
    "18": "reedbuck", 
    "19": "ostrich", 
    "20": "jackal", 
    "21": "mongoose", 
    "22": "eland", 
    "23": "cheetah", 
    "24": "hippopotamus", 
    "25": "insectspider"
}

# Activity name to ID map
ACTIVITIES_NAME2ID = {
    "activity_standing": 0, 
    "activity_moving": 1, 
    "activity_resting": 2, 
    "activity_eating": 3, 
    "activity_interacting": 4
}

# Environments ID to name map
ENVIRONMENTS_ID2NAME = {
    "0": "day", 
    "1": "dawn/dusk", 
    "2": "night", 
    "3": "fog", 
    "4": "snow"
}

# Artificial novel environment orruption severity
ENV_CORRUPTION_SEVERITY = {
    "fog": 2, 
    "snow": 1
}

# Species, activities and environments settings for validation set
VALID_SET = {
    'novel_species_novelty': {
        'species': ['eland', 'koribustard'],
        'activities': ACTIVITIES['known'],
        'environment': ENVIRONMENTS['known']
    },
    'novel_activities_novelty': {
        'species': ['wildebeest', 'topi'],
        'activities': ['Eating'],
        'environment': ENVIRONMENTS['known']
    },
    'novel_environment_novelty': {
        'species': ['zebra', 'wildebeest'],
        'activities': ACTIVITIES['known'],
        'environment': ['dawn/dusk', 'fog', 'snow']
    }
}

# Species, activities and environments settings for test set
TEST_SET = {
    'novel_species_novelty': {
        'species': list(
            set(SPECIES['novel']) - set(VALID_SET['novel_species_novelty']['species'])
            ),
        'activities': ACTIVITIES['known'],
        'environment': ENVIRONMENTS['known']
    },
    'novel_activities_novelty': {
        'species': list(
            set(SPECIES['known']) - set(VALID_SET['novel_activities_novelty']['species'])
            ),
        'activities': ['Eating'],
        'environment': ENVIRONMENTS['known']
    },
    'novel_environment_novelty': {
        'species': list(
            set(SPECIES['known']) - set(VALID_SET['novel_environment_novelty']['species'])
            ),
        'activities': ACTIVITIES['known'],
        'environment': ENVIRONMENTS['novel']
    }
}


