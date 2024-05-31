# This software was created by Oregon State University under Army Research
# Office (ARO) Award Number W911NF-22-2-0149. ARO, as the Federal awarding
# agency, reserves a royalty-free, nonexclusive and irrevocable right to
# reproduce, publish, or otherwise use this software for Federal purposes, and
# to authorize others to do so in accordance with 2 CFR 200.315(b).

import os
import  multiprocessing
import requests
from functools import partial


def __download(image_name, error_files, output_dir):
    # remove appended character to image name of novel environment novelty images
    ss_image_name = image_name[:-5] + image_name[-4:] if image_name[-9].isdigit() else image_name
    save_imge_path = os.path.join(output_dir, image_name.split('/')[-1])
    if not os.path.exists(save_imge_path):
        try:
            image_url = 'https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshotserengeti-unzipped/' + ss_image_name
            img_data = requests.get(image_url).content
            with open(save_imge_path, 'wb') as handler:
                handler.write(img_data)
            # print('donwloading  ', image_name)
        except Exception as ex:
            print(f'{ex} occured when downloading {ss_image_name}')
            error_files.append(image_name)


def download(list_image_urls, output_dir, novelty_type='no_novelty'):
    """
    Download images given list of urls
    """
    errorfiles = []

    a_pool = multiprocessing.Pool()
    download = partial(__download, error_files=errorfiles, output_dir=output_dir)
    result = a_pool.map(download, list_image_urls)

    if novelty_type is None:
        # downloading final NOVEL-SS images
        assert len(errorfiles) == 0
    elif len(errorfiles) > 0:
        # save files that failed to download
        with open(os.path.join(output_dir, novelty_type + '_download_error.txt'), 'w') as fp:
            for item in errorfiles:
                # write each item on a new line
                fp.write("%s\n" % item)
            # print('Done')
