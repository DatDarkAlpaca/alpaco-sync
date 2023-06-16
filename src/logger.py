import logging
import coloredlogs
from src.constants import PUBLIC_FOLDER_NAME


def initialize_logger():
    logging.basicConfig(level=logging.DEBUG, filename=f"./{PUBLIC_FOLDER_NAME}/alpaco-sync.log")

    coloredlogs.install(level='DEBUG')
