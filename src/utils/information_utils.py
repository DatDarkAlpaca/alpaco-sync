import os
import gdown
import logging

from src.utils.json_utils import JsonDB
from src.constants import *


def initialize_public_folder():
    if not os.path.isdir(f"./{PUBLIC_FOLDER_NAME}"):
        os.mkdir(f"./{PUBLIC_FOLDER_NAME}")


def check_sync_file_version() -> bool:
    logging.info('Checking sync file version')

    if not os.path.isfile(f"./{PUBLIC_FOLDER_NAME}/sync-details.json"):
        return False

    __download_sync_file('temp-sync-details.json')
    sync_file = fetch_sync_file()

    temp_sync_filepath = f"./{PUBLIC_FOLDER_NAME}/temp-sync-details.json"
    temp_sync_file = JsonDB(temp_sync_filepath)

    is_best_version = sync_file.data['version'] >= temp_sync_file.data['version']
    if is_best_version:
        os.remove(temp_sync_filepath)

    return is_best_version


def download_public_folder():
    logging.info(f"Downloading files from {SYNC_FOLDER_URL}")
    gdown.download_folder(url=SYNC_FOLDER_URL, output=PUBLIC_FOLDER_NAME, quiet=True, remaining_ok=True)
    logging.info('Finished downloading public files.')


def fetch_sync_file():
    sync_filepath = f"./{PUBLIC_FOLDER_NAME}/{SYNC_FILE_NAME}"
    if os.path.isfile(sync_filepath):
        return JsonDB(sync_filepath)


def __download_sync_file(file_name: str):
    gdown.download(id=SYNC_FILE_ID, output=f"{PUBLIC_FOLDER_NAME}/{file_name}", quiet=True)
