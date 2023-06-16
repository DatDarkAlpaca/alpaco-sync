import shutil
import logging
import os.path
import minecraft_launcher_lib

from src.utils.json_utils import JsonDB
from src.constants import ALPACO_SYNC_PROFILE_NAME, PUBLIC_MODS_FOLDER_NAME


def install_minecraft_version(minecraft_version: str):
    logging.info(f"Installing minecraft {minecraft_version}")
    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
    minecraft_launcher_lib.install.install_minecraft_version(minecraft_version, minecraft_directory)


def install_forge_version(minecraft_version: str):
    forge_version = minecraft_launcher_lib.forge.find_forge_version(minecraft_version)
    if not forge_version:
        logging.error('The forge version specified by the vendor is invalid. Please contact the tool\'s admin')
        return

    logging.info(f"Installing forge {forge_version}")

    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
    minecraft_launcher_lib.forge.install_forge_version(forge_version, minecraft_directory)


def get_forge_version(minecraft_version: str) -> str:
    return minecraft_launcher_lib.forge.find_forge_version(minecraft_version)


def create_custom_profile(forge_version: str, icon_id: str = 'Lectern_Book'):
    logging.info('Creating a custom profile')

    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
    profile_directory = os.path.join(minecraft_directory, 'profiles', ALPACO_SYNC_PROFILE_NAME)

    if not os.path.isdir(profile_directory):
        os.mkdir(profile_directory)

    settings_profile_filepath = os.path.join(minecraft_directory, 'launcher_profiles.json')

    minecraft_version, forge_id = forge_version.split('-')
    sanitized_forge_version = f"{minecraft_version}-forge-{forge_id}"

    settings = JsonDB(settings_profile_filepath)
    settings.data['profiles'].update({
        'alpaco-profile': {
            'gameDir': f"C:\\Users\\paulo\\AppData\\Roaming\\.minecraft\\profiles\\{ALPACO_SYNC_PROFILE_NAME}",
            'icon': icon_id,
            'lastUsed': '2023-06-13T03:01:35.284Z',
            'lastVersionId': sanitized_forge_version,
            'name': ALPACO_SYNC_PROFILE_NAME,
            'type': 'custom'
        }
    })
    settings.save(indent=2)


def install_mods():
    logging.info('Installing required mods')

    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
    profile_directory = os.path.join(minecraft_directory, 'profiles', ALPACO_SYNC_PROFILE_NAME)

    mods_directory = os.path.join(profile_directory, 'mods')
    if os.path.isdir(mods_directory):
        shutil.rmtree(mods_directory, ignore_errors=True)

    shutil.copytree(f"{PUBLIC_MODS_FOLDER_NAME}", mods_directory)
