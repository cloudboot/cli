import requests

from cloudboot.config import CACHE_DIR
from cloudboot.utility.file_manager import read_json_file, file_exists, write_data


def download_template(runtime, trigger):
    file_name = '-'.join([runtime, trigger, 'template.zip'])
    path = '/'.join([CACHE_DIR, file_name])
    if file_exists(path):
        return path
    templates = read_json_file('/'.join([CACHE_DIR, 'templates.json']))
    template_data = requests.get(templates[runtime][trigger])
    write_data(template_data.content, '/'.join([CACHE_DIR, file_name]))
    return path
