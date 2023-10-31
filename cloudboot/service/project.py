from InquirerPy.utils import color_print

from cloudboot.model.DataMap import DataMap
from cloudboot.model.Project import Project
from cloudboot.utility.executor import execute


GCLOUD_PROJECTS = 'gcloud projects'


def list_projects():
    cmd = f'{GCLOUD_PROJECTS} list'
    result = execute(cmd).strip().split('\n')
    if len(result):
        result.pop(0)
    data = DataMap()
    for line in result:
        project = Project(line)
        data.keys.append(project.project_id)
        data.map[project.project_id] = project
    return data


def set_default_project(project_id):
    cmd = f'gcloud config set project {project_id}'
    result = execute(cmd)
    if 'Updated' in result:
        color_print([('yellow', ' '.join(['Default project has been set to', project_id]))])
    return result


def create_project(project_id, project_name, set_as_default=True):
    cmd = f'{GCLOUD_PROJECTS} create {project_id} --name="{project_name}"'
    if set_as_default:
        cmd = f'{cmd} --set-as-default'
    return execute(cmd)
