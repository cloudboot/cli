from InquirerPy.utils import color_print

from cloudboot.config import ROOT_DIR, SRC_DIR, CACHE_DIR
from cloudboot.consts import TEMPLATES, CLOUDBOOT
from cloudboot.enum.ColorCode import ColorCode
from cloudboot.service.core.template import fetch_templates_registry
from cloudboot.utility.executor import execute
from cloudboot.utility.file_manager import path_exists, create_directory
from cloudboot.utility.store import store_exists, rewrite_store


def initialize_cloudboot_project():
    if not path_exists(ROOT_DIR):
        color_print([(ColorCode.ERROR, f'Could not initiate a Cloud Bootstrapper project in {ROOT_DIR}')])
        exit(0)
    if not path_exists(SRC_DIR):
        create_directory(SRC_DIR)
    if not path_exists(CACHE_DIR):
        create_directory(CACHE_DIR)
        create_directory(f'{CACHE_DIR}/{TEMPLATES}')
    if not store_exists(CLOUDBOOT):
        rewrite_store(CLOUDBOOT, {})
    fetch_templates_registry()


def reload_cache():
    fetch_templates_registry()


def ensure_gcloud():
    cmd = 'gcloud --version'
    succeeded, result = execute(cmd)
    if not succeeded:
        color_print([(ColorCode.WARNING, 'Gcloud CLI is not available! Please refer '
                                         'https://cloud.google.com/sdk/docs/install for installation info!')])
        exit(0)
    color_print([(ColorCode.HIGHLIGHT, result)])
