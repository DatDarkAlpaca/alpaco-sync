import re
import jdk
import os
import logging
import subprocess
from pathlib import Path

from src.utils.environment_variables import append_to_environment_variables, set_environment_variable


def get_installed_java_version() -> str | None:
    try:
        java_version = subprocess.check_output('java -version', stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError:
        return None

    version_string, _ = re.search('\"(\d+\.\d+).*\"', java_version.decode()).groups()[0].split('.')
    return version_string


def install_java_version(version: str) -> None:
    java_path = os.path.join(str(Path.home()), '.jdk')
    jdk.install(version, path=java_path)

    java_version_path = None
    for directory in os.listdir(java_path):
        if str(version) in directory:
            java_version_path = os.path.join(java_path, directory)

    if not java_version_path:
        logging.error('No JDK directory found. Try installing Java again.')
        return

    java_home = java_version_path
    java_bin_home = os.path.join(java_home, 'bin')

    set_environment_variable('JAVA_HOME', java_home)
    append_to_environment_variables(java_bin_home)
