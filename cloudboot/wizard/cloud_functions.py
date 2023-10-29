from InquirerPy import inquirer
from InquirerPy.utils import color_print

from cloudboot.enum.Common import Runtime, Trigger
from cloudboot.model.CloudFunctionConfig import CloudFunctionConfig
from cloudboot.service.cloud_functions import list_runtimes, init_function_sources, list_regions, \
    set_default_functions_region
from cloudboot.utility.store import retrieve_data, store_data, data_exists

CLOUD_FUNCTIONS_STORE = 'cloud_functions'
DEFAULT_CONFIG_STORE = 'default_config'
DEFAULT_REGION = 'cloud_functions_region'


def cloud_functions():
    default_config = retrieve_data(DEFAULT_CONFIG_STORE)
    color_print([('yellow', '<<<- New Cloud Function ->>>')])
    name = inquirer.text(message='Name', default='my-function').execute()
    default_region = inquirer.confirm(
        message='Use default region?',
        default=True
    )
    region = None
    if default_region:
        region = default_config[DEFAULT_REGION]
    if not region or not default_region:
        regions = list_regions()
        selected_region = inquirer.select(
            message='Select region',
            choices=regions,
            default=regions[0]
        )
        if not region:
            region = selected_region
        if default_region:
            default_config[DEFAULT_REGION] = selected_region
            store_data(DEFAULT_CONFIG_STORE, default_config)
            set_default_functions_region(selected_region)
    runtime_prefix = inquirer.select(
        message='Select runtime environment',
        choices=list(map(str, Runtime)),
        default=Runtime.PYTHON
    ).execute()
    runtimes = list_runtimes(runtime_prefix)
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
    }[trigger]
    if trigger_name:
        trigger_name = trigger_name.execute()
    init_function_sources(name, runtime, trigger)
    cloud_function_config = CloudFunctionConfig(name, runtime, runtime_prefix)
    cloud_function_config.set_trigger_config(trigger, trigger_name)
    cloud_function_config.set_region_config(region)
    if not data_exists(CLOUD_FUNCTIONS_STORE):
        store_data(CLOUD_FUNCTIONS_STORE, {})
    instances = retrieve_data(CLOUD_FUNCTIONS_STORE)
    instances[cloud_function_config.name] = cloud_function_config.__dict__
    store_data(CLOUD_FUNCTIONS_STORE, instances)
