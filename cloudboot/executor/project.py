from cloudboot.enum.Common import Common
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


def set_project(project):
    cmd = ' '.join([
        Common.GCLOUD,
        Property.CONFIG,
        Operation.SET,
        Property.PROJECT,
        project
    ])
    result = execute(cmd)
    return result
