from cloudboot.config import ROOT_DIR
from cloudboot.utility.file_manager import read_json_file, write_json_file


def load_settings():
    return read_json_file('/'.join([ROOT_DIR, 'cloudboot.json']))


def write_settings(data):
    return write_json_file(data, '/'.join([ROOT_DIR, 'cloudboot.json']))
