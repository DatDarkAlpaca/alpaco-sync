from utils.information_utils import *
from utils.java_utils import *

from logger import initialize_logger
from utils.minecraft_utils import *


def main():
    initialize_public_folder()
    initialize_logger()

    # Drive:
    if not check_sync_file_version():
        download_public_folder()
    sync_file = fetch_sync_file()

    # Java:
    installed_java_version = get_installed_java_version()
    required_java_version = sync_file.data['java-version']
    if not installed_java_version or required_java_version != installed_java_version:
        logging.error(f"The appropriate JDK is not installed in this machine. "
                      f"Installing JDK {required_java_version}")
        install_java_version(required_java_version)

    else:
        logging.info('The current java version matches the requirements. Proceeding with the installation')

    # Minecraft:
    required_minecraft_version = sync_file.data['minecraft-version']

    if not check_if_minecraft_version_installed(required_minecraft_version):
        logging.error('You do not have the required minecraft version. Installing.')
        install_minecraft_version(required_minecraft_version)

    latest_forge_version = get_latest_forge_version(required_minecraft_version)
    if not check_if_latest_forge_version_installed(required_minecraft_version):
        logging.error('You do not have the required forge version. Installing.')
        install_forge_version(required_minecraft_version)

    create_custom_profile(latest_forge_version)
    install_mods()


if __name__ == '__main__':
    main()
