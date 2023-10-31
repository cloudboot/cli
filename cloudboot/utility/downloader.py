import requests

from cloudboot.config import CACHE_DIR, TEMPLATES_STORE
from cloudboot.utility.file_manager import write_data, file_exists
from cloudboot.utility.store import get_store

TEMPLATE_DIR = 'templates'


def download_template(service_type, runtime_prefix, trigger):
    file_name = f'{service_type}-{runtime_prefix}-{trigger}-template.zip'
    path = f'{CACHE_DIR}/{TEMPLATE_DIR}/{file_name}'
    if file_exists(path):
        return path
    templates = get_store(TEMPLATES_STORE)
    template_data = requests.get(templates[service_type][runtime_prefix][trigger])
    write_data(template_data.content, path)
    return path
