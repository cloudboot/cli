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


def extract_zip_file(source, target):
    create_directory(target)
    sub_dir = None
    with ZipFile(source) as archive:
        archive.extractall(target)
        archive_files = archive.namelist()
        sub_dir = archive_files[0] if all(item.startswith(archive_files[0]) for item in archive_files) else None
    if sub_dir:
        sub_dir = f'{target}/{sub_dir}'
        os.system(f'mv {sub_dir}/* {target}/')
        shutil.rmtree(sub_dir)


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
