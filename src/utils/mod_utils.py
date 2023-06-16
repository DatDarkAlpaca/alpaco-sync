import zipfile
from dataclasses import dataclass


@dataclass
class ModInfo:
    name: str
    version: str


def zip_file_contains(filepath: str, target_path: str) -> bool:
    f = zipfile.ZipFile(filepath, 'r')
    result = any(x.startswith(target_path.rstrip('/')) for x in f.namelist())
    f.close()

    return result


def get_mod_info(filepath: str) -> ModInfo:
    manifest_filepath = 'META-INF/MANIFEST.MF'

    if not zip_file_contains(filepath, manifest_filepath):
        return ModInfo('', '')

    with zipfile.ZipFile(filepath, mode='r') as zip_file:
        mod_name, mod_version = [''] * 2

        with zip_file.open(manifest_filepath) as manifest_file:
            for line in manifest_file.readlines():
                line_str = line.decode().strip().replace('\n', '')
                if not line_str:
                    continue

                if ':' not in line_str:
                    continue

                key, value = line_str.replace('\n', '').split(':', maxsplit=1)

                if key.lower() == 'specification-title':
                    mod_name = value.lower().strip()

                elif key.lower() == 'implementation-version':
                    mod_version = value.lower().strip()

        return ModInfo(mod_name, mod_version)
