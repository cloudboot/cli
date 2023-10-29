import pickle
from os.path import isfile

from cloudboot.config import CACHE_DIR


def store_data(name, obj):
    with open(f'{CACHE_DIR}/{name}.pickle', 'wb') as file_obj:
        pickle.dump(obj, file_obj)


def retrieve_data(name):
    with open(f'{CACHE_DIR}/{name}.pickle', 'rb') as file_obj:
        return pickle.load(file_obj)


def data_exists(name):
    return isfile(f'{CACHE_DIR}/{name}.pickle')
