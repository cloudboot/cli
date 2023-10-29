from InquirerPy.utils import color_print

from cloudboot.enum.Common import Common, Args
from cloudboot.enum.Crud import Crud
from cloudboot.enum.Operation import Operation
from cloudboot.enum.Property import Property
from cloudboot.model.DataMap import DataMap
from cloudboot.model.Project import Project
from cloudboot.utility.executor import execute


def list_projects():
    cmd = ' '.join([
        Common.GCLOUD,
        Property.PROJECTS,
        Crud.LIST
    ])
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
    cmd = ' '.join([
        Common.GCLOUD,
        Property.CONFIG,
        Operation.SET,
        Property.PROJECT,
        project_id
    ])
    result = execute(cmd)
    if 'Updated' in result:
        color_print([('yellow', ' '.join(['Default project has been set to', project_id]))])
    return result


def create_project(project_id, project_name, set_as_default=True):
    cmd = ' '.join([
        Common.GCLOUD,
        Property.PROJECTS,
        Crud.CREATE,
        project_id,
        '='.join([Args.NAME, f'"{project_name}"']),
    ])
    if set_as_default:
        cmd = ' '.join([cmd, Args.SET_AS_DEFAULT])
    return execute(cmd)
