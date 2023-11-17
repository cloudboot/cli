import json
from os.path import isfile

from cloudboot.config import CACHE_DIR


def rewrite_store(name, obj):
    """ Rewrite or create json files

    Helper function to store/rewrite Cloud bootstrapper cache and configuration files  related to the current workspace.

    Parameters
    -----------------
    name: str
        Name of the JSON file, without file type and path.
    obj: any
        Object to store.
    """
    with open(f'{CACHE_DIR}/{name}.json', 'w+') as file_obj:
        json.dump(obj, file_obj, indent=4)


def get_store(name):
    """ Retrieve json files

    Helper function to store Cloud bootstrapper cache and configuration files related to the current workspace.

    Parameters
    -----------------
    name: str
        Name of the JSON file, without file type and path.

    """
    with open(f'{CACHE_DIR}/{name}.json', 'r') as file_obj:
        return json.load(file_obj)


def store_exists(name):
    """ Check whether the json file exists

    Helper function to check the availability of a JSON file.

    Parameters
    -----------------
    name: str
        Name of the JSON file, without file type and path.
    """
    return isfile(f'{CACHE_DIR}/{name}.json')
