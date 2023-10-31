import json

import requests
from InquirerPy.utils import color_print

from cloudboot.config import ROOT_DIR, SRC_DIR, CACHE_DIR, CLOUDBOOT_CONFIG, TEMPLATES_REGISTRY_URL, TEMPLATES_STORE
from cloudboot.utility.file_manager import path_exists, create_directory
from cloudboot.utility.store import store_exists, rewrite_store


def fetch_template_registry():
    response = requests.get(TEMPLATES_REGISTRY_URL)
    if not store_exists(TEMPLATES_STORE):
        rewrite_store(TEMPLATES_STORE, json.loads(response.content))


def initialize_cloudboot_project():
    if not path_exists(ROOT_DIR):
        color_print([('red', f'Could not initiate a cloudboot project in {ROOT_DIR}')])
        exit(0)
    if not path_exists(SRC_DIR):
        create_directory(SRC_DIR)
    if not path_exists(CACHE_DIR):
        create_directory(CACHE_DIR)
        create_directory(f'{CACHE_DIR}/{TEMPLATES_STORE}')
    if not store_exists(CLOUDBOOT_CONFIG):
        rewrite_store(CLOUDBOOT_CONFIG, {})
    fetch_template_registry()
