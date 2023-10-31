from InquirerPy import inquirer
from InquirerPy.base import Choice
from InquirerPy.utils import color_print

from cloudboot.config import CLOUDBOOT_CONFIG
from cloudboot.enum.Common import Runtime, Trigger
from cloudboot.model.CloudFunctionConfig import CloudFunctionConfig
from cloudboot.service.cloud_functions import list_runtimes, init_function_sources, list_regions, \
    set_default_functions_region, get_local_functions_list, deploy_function
from cloudboot.utility.store import get_store, rewrite_store, store_exists

CLOUD_FUNCTIONS_STORE = 'cloud_functions'
DEFAULT_REGION = 'cloud_functions_region'


def init_cloud_function():
    cloudboot_config = get_store(CLOUDBOOT_CONFIG)
    color_print([('yellow', '<<<- New Cloud Function ->>>')])
    name = inquirer.text(message='Name', default='my-function').execute()
    default_region = inquirer.confirm(
        message='Use default region?',
        default=True
    ).execute()
    region = None
    if default_region and DEFAULT_REGION in cloudboot_config:
        region = cloudboot_config[DEFAULT_REGION]
    if not region:
        regions = list_regions()
        region = inquirer.select(
            message='Select region',
            choices=regions,
            default=regions[0]
        ).execute()
        if default_region:
            cloudboot_config[DEFAULT_REGION] = region
            rewrite_store(CLOUDBOOT_CONFIG, cloudboot_config)
            set_default_functions_region(region)
    runtime_prefix = inquirer.select(
        message='Select runtime environment',
        choices=list(map(str, Runtime)),
        default=Runtime.PYTHON
    ).execute()
    runtimes = list_runtimes(runtime_prefix, region)
    runtime = inquirer.select(
        message=f'Select {runtime_prefix} version',
        choices=runtimes,
        default=runtimes[0]
    ).execute()
    trigger = inquirer.select(
        message="Select function trigger",
        choices=list(map(str, Trigger)),
        default=Trigger.HTTPS
    ).execute()
    trigger_name = {
        Trigger.PUBSUB: inquirer.text(message='Topic name'),
        Trigger.STORAGE: inquirer.text(message='Bucket')
    }
    if hasattr(trigger_name, trigger):
        trigger_name = trigger_name[trigger].execute()
    else:
        trigger_name = None
    init_function_sources(name, runtime_prefix, trigger)
    cloud_function_config = CloudFunctionConfig(name, runtime, runtime_prefix)
    cloud_function_config.set_trigger_config(trigger, trigger_name)
    cloud_function_config.set_region_config(region)
    if not store_exists(CLOUD_FUNCTIONS_STORE):
        rewrite_store(CLOUD_FUNCTIONS_STORE, {})
    instances = get_store(CLOUD_FUNCTIONS_STORE)
    instances[cloud_function_config.name] = cloud_function_config.__dict__
    rewrite_store(CLOUD_FUNCTIONS_STORE, instances)


def select_and_deploy_function():
    functions = get_local_functions_list()
    function = inquirer.select(
        message='Select cloud function',
        choices=[Choice(name=key, value=value) for key, value in functions.items()]
    ).execute()
    deploy_function(function)
