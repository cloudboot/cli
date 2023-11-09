from InquirerPy import inquirer
from InquirerPy.base import Choice
from InquirerPy.utils import color_print

from cloudboot.consts import CLOUDBOOT
from cloudboot.enum.CloudService import CloudService
from cloudboot.enum.CloudServiceRuntime import CloudServiceRuntime
from cloudboot.enum.CloudServiceTrigger import CloudServiceTrigger
from cloudboot.enum.ColorCode import ColorCode
from cloudboot.model.CloudFunctionConfig import CloudFunctionConfig
from cloudboot.service.gcloud.cloud_functions import list_runtimes, init_function_sources, list_regions, \
    set_default_functions_region, get_local_functions_list, deploy_function
from cloudboot.utility.store import get_store, rewrite_store, store_exists

DEFAULT_REGION = f'{CloudService.CLOUD_FUNCTIONS}_region'


def init_cloud_function():
    cloudboot_config = get_store(CLOUDBOOT)
    color_print([(ColorCode.HIGHLIGHT, '<<<- New Cloud Function ->>>')])
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
            rewrite_store(CLOUDBOOT, cloudboot_config)
            set_default_functions_region(region)
    runtime_prefix = inquirer.select(
        message='Select runtime environment',
        choices=list(map(str, CloudServiceRuntime)),
        default=CloudServiceRuntime.PYTHON
    ).execute()
    runtimes = list_runtimes(runtime_prefix, region)
    runtime = inquirer.select(
        message=f'Select {runtime_prefix} version',
        choices=runtimes,
        default=runtimes[0]
    ).execute()
    trigger = inquirer.select(
        message="Select function trigger",
        choices=list(map(str, CloudServiceTrigger)),
        default=CloudServiceTrigger.HTTP
    ).execute()
    print(trigger)
    trigger_name = {
        CloudServiceTrigger.FIRESTORE: inquirer.text(message='Database'),
        CloudServiceTrigger.PUBSUB: inquirer.text(message='Topic'),
        CloudServiceTrigger.STORAGE: inquirer.text(message='Bucket')
    }
    if trigger in trigger_name.keys():
        trigger_name = trigger_name[trigger].execute()
    else:
        trigger_name = None
    init_function_sources(name, runtime_prefix, trigger)
    cloud_function_config = CloudFunctionConfig(name, runtime, runtime_prefix)
    cloud_function_config.set_trigger_config(trigger, trigger_name)
    cloud_function_config.set_region_config(region)
    if not store_exists(CloudService.CLOUD_FUNCTIONS):
        rewrite_store(CloudService.CLOUD_FUNCTIONS, {})
    instances = get_store(CloudService.CLOUD_FUNCTIONS)
    instances[cloud_function_config.name] = cloud_function_config.__dict__
    rewrite_store(CloudService.CLOUD_FUNCTIONS, instances)


def select_and_deploy_function():
    functions = get_local_functions_list()
    if len(functions) == 0:
        color_print([(ColorCode.INFO, 'Local cloud function directory is empty!')])
        return
    function = inquirer.select(
        message='Select cloud function',
        choices=[Choice(name=key, value=value) for key, value in functions.items()]
    ).execute()
    deploy_function(function)
