from InquirerPy import inquirer

from cloudboot.config import cloud_functions_runtimes, cloud_functions_triggers
from cloudboot.executor.cloud_function import create_function


def cloud_functions_wizard():
    name = inquirer.text(message="New function name:", default='my-function').execute()
    runtime = inquirer.select(
        message="Select runtime environment:",
        choices=cloud_functions_runtimes,
        default=cloud_functions_runtimes[0]
    ).execute()
    trigger = inquirer.select(
        message="Select function trigger:",
        choices=cloud_functions_triggers,
        default=cloud_functions_triggers[0]
    ).execute()
    create_function(name, runtime, trigger)
