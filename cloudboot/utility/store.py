import pickle
from os.path import isfile

from cloudboot.config import CACHE_DIR


def rewrite_store(name, obj):
    with open(f'{CACHE_DIR}/{name}.pickle', 'wb') as file_obj:
        pickle.dump(obj, file_obj)


def get_store(name):
    with open(f'{CACHE_DIR}/{name}.pickle', 'rb') as file_obj:
        return pickle.load(file_obj)


def store_exists(name):
    return isfile(f'{CACHE_DIR}/{name}.pickle')
