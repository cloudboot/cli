import json
import os
from os.path import isfile
from zipfile import ZipFile


def file_exists(path):
    return isfile(path)


def read_json_file(path):
    if not file_exists(path):
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
    with ZipFile(source) as archive:
        archive.extractall(target)


def create_directory(path):
    os.makedirs(path)
