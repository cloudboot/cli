from InquirerPy import inquirer
from InquirerPy.utils import color_print

from cloudboot.consts import CLOUDBOOT
from cloudboot.enum.ColorCode import ColorCode
from cloudboot.service.gcloud.project import list_projects, create_project, set_default_project, project_exists
from cloudboot.utility.store import rewrite_store


def init_cloud_project():
    project = None
    existing_project = inquirer.confirm(message='Use existing project?', default=True).execute()
    if existing_project:
        projects = list_projects()
        if not projects.is_empty():
            project_choices = projects.choices()
            project = inquirer.select(message='Select a project:', choices=project_choices,
                                      default=project_choices[0].value if len(project_choices) > 0 else None
                                      ).execute()
        if project:
            set_default_project(project['projectId'])
    if not project:
        color_print([(ColorCode.HIGHLIGHT, '<<<- Create new project ->>>')])
        project_id = inquirer.text(message="Project Id:").execute()
        project_name = inquirer.text(message="Project Name:", default='My New Serverless Project').execute()
        set_default = inquirer.confirm(message="Set new project as default project", default=True).execute()
        create_project(project_id, project_name, set_default)
        project = project_exists(project_id)
        if project:
            color_print([('yellow', f'Successfully initiated the project {project["projectId"]}')])
    if not project:
        color_print([(ColorCode.ERROR, 'Something went wrong while trying to set up the project!')])
        exit(0)
    else:
        rewrite_store(CLOUDBOOT, {'default_cloud_project': project['projectId']})
