from InquirerPy import inquirer
from InquirerPy.utils import color_print

from cloudboot.executor.project import list_projects


def initialize_project_wizard():
    project = None
    existing_project = inquirer.confirm(
        message='Use existing project?',
        default=True
    ).execute()
    if existing_project:
        projects = list_projects()
        project_choices = projects.choices()
        project = inquirer.select(
            message='Select a project:',
            choices=project_choices,
            default=project_choices[0] if len(project_choices) > 0 else None
        ).execute()
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



