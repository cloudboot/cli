import hashlib
import json
import os
import shutil
from os.path import isfile, isdir
from zipfile import ZipFile


def path_exists(path):
    return isdir(path)


def file_exists(path):
    return isfile(path)


def read_json_file(path):
    if not path_exists(path):
        write_json_file({}, path)
    with open(path, 'r') as file_obj:
        return json.load(file_obj)


def write_json_file(data, path):
    with open(path, 'w') as file_obj:
        json.dump(data, file_obj)


def write_data(content, path):
    with open(path, 'wb') as file_obj:
        return file_obj.write(content)


def extract_zip_file(source, target, src_dir=None):
    create_directory(target)
    with ZipFile(source) as archive:
        archive.extractall(target)
    if src_dir:
        src_dir = f'{target}/{src_dir}'
        os.system(f'mv {src_dir}/* {target}/')
        shutil.rmtree(src_dir)


def create_directory(path):
    os.makedirs(path)


def calculate_checksum(path):
    """Calculates the checksum of a file.

    Args:
      path: The path to the file.

    Returns:
      The checksum of the file.
    """
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def directory_checksum(path):
    checksum = ""
    for root, dirs, files in os.walk(path):
        for filename in files:
            file_checksum = calculate_checksum(os.path.join(root, filename))
            checksum += file_checksum
