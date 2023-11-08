import requests

from cloudboot.config import CACHE_DIR
from cloudboot.model.Template import Template
from cloudboot.utility.file_manager import write_data, file_exists

TEMPLATE_DIR = 'templates'


def download_template(template_config: Template):
    file_name = f'{template_config.name}-template.zip'
    path = f'{CACHE_DIR}/{TEMPLATE_DIR}/{file_name}'
    if file_exists(path):
        return path
    template_data = requests.get(template_config.src)
    write_data(template_data.content, path)
    return path
