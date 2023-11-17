import os

ROOT_DIR = os.getcwd()
SRC_DIR = f'{ROOT_DIR}/src'
CACHE_DIR = f'{ROOT_DIR}/.cloudboot'

TEMPLATES_REGISTRY_URL = 'https://raw.githubusercontent.com/cloudboot/template-registry/main/index.json'


def reset_root(path=os.getcwd()):
    """ Reset the workspace directory.

    This function will set the working directory which includes Cloud bootstrapper configuration files, cache
    and project sources.

    parameters:
    path: str, optional
        Current directory will be taken from where cloudboot command runs.
    """
    global ROOT_DIR, SRC_DIR, CACHE_DIR, CLOUDBOOT_CONFIG
    ROOT_DIR = path
    SRC_DIR = f'{ROOT_DIR}/src'
    CACHE_DIR = f'{ROOT_DIR}/.cloudboot'
