from InquirerPy import inquirer
from InquirerPy.utils import color_print

from cloudboot.service.project import list_projects, create_project, set_default_project
from cloudboot.model.Project import Project
from cloudboot.utility.settings import write_settings


def initialize_project_wizard():
    project = None
    existing_project = inquirer.confirm(
        message='Use existing project?',
        default=True
    ).execute()
    if existing_project:
        projects = list_projects()
        project_choices = projects.choices()
        project: Project = inquirer.select(
            message='Select a project:',
            choices=project_choices,
            default=project_choices[0].value if len(project_choices) > 0 else None
        ).execute()
        if project:
            set_default_project(project.project_id)
    if not project:
        color_print([('yellow', '<<<- Create new project ->>>')])
        project_id = inquirer.text(
            message="Project Id:"
        ).execute()
        project_name = inquirer.text(
            message="Project Name:",
            default='My New Serverless Project'
        ).execute()
        set_default = inquirer.confirm(
            message="Set new project as default project?",
            default=True
        ).execute()
        result = create_project(project_id, project_name, set_default)
        if 'finished' in result:
            projects = list_projects()
            if projects.keys[project_id]:
                project = projects.map[project_id]
                color_print([('yellow',
                              f'Successfully initiated the project {project.project_id}:{project.project_number}')])
    if not project:
        color_print([('#ffc1cc', 'Something went wrong while trying to set up the project!')])
        exit(0)
    else:
        write_settings({
            'project_id': project.project_id
        })
