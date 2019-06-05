# 
# Copyright 2018 Kionix Inc.
#
import json
import os
from argparse import ArgumentParser
from zipfile import ZipFile
import shutil

from google.oauth2 import service_account
from google.cloud import storage


# python get_configs.py cfg\configurations-reader.json

EXTENSIONS = ['.JSON', '.json', '.TXT', '.txt', '.xml', '.XML']
PROJECT_ID = 'rokix-configuration-releases'


def get_configs(service_account_json_file, zip_filename='board_and_stream_cfg.zip', extract_dir='cfg'):
    '''
        Downloads and extracts board configurations from GCP
    '''
    with open(service_account_json_file, 'r') as sa_file:
        bucket_name = json.load(sa_file)['bucket']
    credentials = service_account.Credentials.from_service_account_file(
        args.sa_account_json_key)
    client = storage.Client(project=PROJECT_ID, credentials=credentials)
    bucket = storage.Bucket(client, bucket_name)
    configs = bucket.get_blob(zip_filename)
    configs.download_to_filename(zip_filename)

    with ZipFile(zip_filename) as zip_file:
        try:
            for member in zip_file.namelist():
                path, file_name = os.path.split(member)
                if os.path.splitext(file_name)[1] in EXTENSIONS and path == 'board_config':
                    file_loc = zip_file.extract(member, extract_dir)
                    shutil.move(file_loc, os.path.join(extract_dir, os.path.basename(file_loc)))
                else:
                    zip_file.extract(member, extract_dir)
        finally:
            shutil.rmtree(os.path.join(extract_dir, 'board_config'))


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument(
        'sa_account_json_key',
        default='cfg/configurations-reader.json',
        nargs='?',
        help='Service account json key file'
    )
    args = parser.parse_args()
    get_configs(args.sa_account_json_key)
