import json
from os.path import isfile

from cloudboot.config import CACHE_DIR


def rewrite_store(name, obj):
    with open(f'{CACHE_DIR}/{name}.json', 'w') as file_obj:
        json.dump(obj, file_obj, indent=4)


def get_store(name):
    with open(f'{CACHE_DIR}/{name}.json', 'r') as file_obj:
        return json.load(file_obj)


def store_exists(name):
    return isfile(f'{CACHE_DIR}/{name}.json')
