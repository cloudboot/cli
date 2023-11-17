import json

from InquirerPy.utils import color_print

from cloudboot.consts import GCLOUD_CLI_FLAGS
from cloudboot.enum.ColorCode import ColorCode
from cloudboot.model.DataMap import DataMap
from cloudboot.utility.executor import execute

GCLOUD_PROJECTS = 'gcloud projects'


def list_projects():
    data = DataMap('projectId', 'name')
    cmd = f'{GCLOUD_PROJECTS} list {GCLOUD_CLI_FLAGS}'
    succeeded, result = execute(cmd)
    if succeeded:
        result = json.loads(result)
        if len(result):
            data.push_all(result)
    return data


def set_default_project(project_id):
    cmd = f'gcloud config set project {project_id}'
    succeeded, result = execute(cmd)
    if not succeeded:
        return False
    if 'Updated' in result:
        color_print([(ColorCode.HIGHLIGHT, ' '.join(['Default project has been set to', project_id]))])
    return result


def create_project(project_id, project_name, set_as_default=True):
    cmd = f'{GCLOUD_PROJECTS} create {project_id} --name="{project_name}"'
    if set_as_default:
        cmd = f'{cmd} --set-as-default'
    cmd = f'{cmd} {GCLOUD_CLI_FLAGS}'
    succeeded, result = execute(cmd)
    if not succeeded:
        return False
    return result


def project_exists(project_id):
    cmd = f'{GCLOUD_PROJECTS} describe {project_id} {GCLOUD_CLI_FLAGS}'
    succeeded, result = execute(cmd)
    if succeeded:
        result = json.loads(result)
        return result
    return False
