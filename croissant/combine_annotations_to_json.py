# This software was created by Oregon State University under Army Research
# Office (ARO) Award Number W911NF-22-2-0149. ARO, as the Federal awarding
# agency, reserves a royalty-free, nonexclusive and irrevocable right to
# reproduce, publish, or otherwise use this software for Federal purposes, and
# to authorize others to do so in accordance with 2 CFR 200.315(b).

import os
import ast
import numpy as np
import pandas as pd
import zipfile
import shutil
import json

from config.config import SS_URL


def zipdir(path, ziph):
        # ziph is zipfile handle
        abs_src = os.path.abspath(path)
        for root, dirs, files in os.walk(path):
            for file in files:
                absname = os.path.join(root, file)
                arcname = absname[len(abs_src) + 1:]
                # ziph.write(absname, arcname)
                ziph.write(
                    absname, 
                    os.path.relpath(
                        absname, 
                        path
                        # os.path.join(path, '..')
                    )
                )
                

def unzip_label_obj(zip_file_path, output_dir):
    """
    Extract object filename into output_dir directory
    Arguments:
        zip_file_path: path to zip file
        output_dir: directory to extract to
    """
    assert os.path.exists(zip_file_path)
    assert zip_file_path[-4:] == '.zip'
    assert os.path.exists(output_dir)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)


def merge_annotations_n_bbox(path_to_zipped_labels=None, output_dir=None, save_as_jsonl=True):

    if path_to_zipped_labels is None:
        path_to_zipped_labels='labels/novel_ss_labels.zip'
        # output_dir='labels/cr_json_annotations/'
        output_dir='labels/croissant_jsonl/'
    elif output_dir is None:
        split_zip_path = path_to_zipped_labels.split('/')
        # if len(split_zip_path) <= 1:
        #     output_dir = 'cr_json_annotations/'
        # else:
        #     output_dir = os.join.path('/'.join(split_zip_path[:-1]), 'cr_json_annotations/')
        output_dir = os.join.path('/'.join(split_zip_path[:-1]), 'croissant_jsonl/')

    assert os.path.exists(path_to_zipped_labels)
    os.makedirs(output_dir, exist_ok=True)

    unzip_label_obj(path_to_zipped_labels, output_dir)

    for set_name in ['train', 'valid', 'test']:
        path_csv = os.path.join(output_dir, set_name + '.csv')
        df_set = pd.read_csv(path_csv, low_memory=False)
        df_set = df_set.sample(frac=1)  # shuffle rows

        path_json = os.path.join(output_dir, set_name + '.json')
        path_jsonl = os.path.join(output_dir, set_name + '.jsonl')
        bboxes_set = json.load(open(path_json))

        # dict_set = df_set.to_dict('index')
        df_set = df_set.replace({np.nan: None})
        dict_set = df_set.where((pd.notnull(df_set)), None).to_dict('index')

        for k in dict_set.keys():
            # ** change string representation of list into list
            # dict_set[k]['ss_url'] = SS_URL + dict_set[k]['image_path']
            # dict_set[k]['bboxes'] = bboxes_set[dict_set[k]['filename']]
            '''
            dict_set[k]['activities'] = ast.literal_eval(dict_set[k]['activities'])
            dict_set[k]['activities_id'] = ast.literal_eval(dict_set[k]['activities_id'])
            dict_set[k]['bboxes'] = []
            for bbox in enumerate(bboxes_set[dict_set[k]['filename']]):
                dict_set[k]['bboxes'].append(
                    {"bbox": bbox}
                )
            '''
            dict_set[k]['bboxes'] = str(bboxes_set[dict_set[k]['filename']])

            if 'master_id' in dict_set[k]:
                del dict_set[k]['master_id']

        dict_set = list(dict_set.values())

        if save_as_jsonl:
            with open(path_jsonl, 'w') as outfile:
                for entry in dict_set:
                    json.dump(entry, outfile)
                    outfile.write('\n')
            os.remove(path_json)
        else:
            # overwrite unzipped json file and delete csv file
            with open(path_json, "w") as outfile:
                json.dump(dict_set, outfile)
        os.remove(path_csv)
    
    ''''''
    if save_as_jsonl:
        # create a zip file of the combined json annotations
        with zipfile.ZipFile(os.path.dirname(path_jsonl)+'.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipdir(os.path.dirname(path_jsonl), zipf)

        # remove created dir containing combined json and keep compressed obj
        try:
            shutil.rmtree(os.path.dirname(path_jsonl))
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    else:
        # create a zip file of the combined json annotations
        with zipfile.ZipFile(os.path.dirname(path_json)+'.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipdir(os.path.dirname(path_json), zipf)

        # remove created dir containing combined json and keep compressed obj
        try:
            shutil.rmtree(os.path.dirname(path_json))
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    ''''''
        



if __name__ == "__main__":
    pass
