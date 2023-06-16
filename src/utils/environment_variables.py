import logging
import os
import subprocess

# Todo: do a linux solution.


def append_to_environment_variables(path: str):
    system_path = os.path.abspath(path)
    subprocess.check_output(f'setx /M path "%path%;{system_path}"', shell=True)


def set_environment_variable(variable_name: str, value: str) -> None:
    if variable_name.lower() in ['path', 'tmp', 'temp', 'comspec',
                                 'driverdata', 'number_of_processors', 'os',
                                 'pathext', 'processor_architecture', 'processor_identifier', 'processor_level',
                                 'processor_revision', 'PSModulePath', 'username', 'windir', 'zes_enable_sysmain']:
        logging.error('Please use the safe alternative to change system variables.')
        return

    subprocess.check_output(f"setx /M {variable_name} {value}", shell=True)
