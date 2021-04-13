# Loading Libraries & Packages
import os
import glob

import argparse

import tqdm

import requests
import json


# Creating Directory for Subject
def create_dir(id):
    if not os.path.exists(f'data/raw/{id}'):
        os.makedirs(f'data/raw/{id}')


# List IDs of all scans of a given Subject
def subject_scans(id):
    response = requests.get(f'http://dev-main.abhayparimitii.cloudns.asia/userdata/scaninfo/{id}')
    scan_ids = [i['scan_id'] for i in response.json()['scan_info']]
    return scan_ids

# Dumping all scans of a Subject in Directory
def dump_scans(id):
    create_dir(id)
    scans_ids = subject_scans(id)  
    pbar = tqdm.tqdm(scans_ids)
    for scan in pbar:
        pbar.set_description("Processing %s" % scan)
        scan_response = requests.get(f'http://dev-main.abhayparimitii.cloudns.asia/userdata/getinfo/{scan}')
        scan_response_json = scan_response.json()
        with open('data/' + f'{id}' + '/' + f'{scan}.json', 'w', encoding='utf-8') as f:
            json.dump(scan_response_json, f, ensure_ascii=False, indent=4)
    print('\n')
    print('All Scans Dumped!')


if __name__ == "__main__":
    # initialize ArgumentParser class of argparse
    parser = argparse.ArgumentParser()

    # currently, we only need filepath to the image
    parser.add_argument("--subject_id", type=str)

    # read the arguments from the command line
    args = parser.parse_args()

    # run the predict specified by command line arguments
    dump_scans(id=args.subject_id)


    
