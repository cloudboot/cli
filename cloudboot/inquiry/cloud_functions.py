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
    set_default_functions_region, get_local_functions_list, get_functions_event_types, \
    list_available_functions_templates, deploy_selected_function
from cloudboot.service.gcloud.firestore import list_firestore_databases, list_firestore_database_locations
from cloudboot.service.gcloud.pubsub import list_pubsub_topics
from cloudboot.service.gcloud.storage import list_storage_buckets
from cloudboot.utility.store import get_store, rewrite_store, store_exists

DEFAULT_REGION = f'{CloudService.CLOUD_FUNCTIONS}_region'

trigger_selector = {
    CloudServiceTrigger.FIRESTORE: {
        'new': inquirer.text(message='New Firestore database name'),
        'list': list_firestore_databases
    },
    CloudServiceTrigger.PUBSUB: {
        'new': inquirer.text(message='New PubSub Topic name'),
        'list': list_pubsub_topics
    },
    CloudServiceTrigger.STORAGE: {
        'new': inquirer.text(message='New Storage Bucket name'),
        'list': list_storage_buckets
    }
}


def select_function_region(cloudboot_config: dict):
    selected_region = None
    use_default_region = inquirer.confirm(message='Use default region?', default=True).execute()
    if use_default_region and DEFAULT_REGION in cloudboot_config:
        selected_region = cloudboot_config[DEFAULT_REGION]
    elif DEFAULT_REGION not in cloudboot_config:
        color_print([(ColorCode.WARNING, 'Default region configuration does not exists!')])
    if not selected_region:
        regions = list_regions()
        region_choices = regions.choices()
        region = inquirer.select(message='Select region', choices=region_choices,
                                 default=region_choices[0].value).execute()
        selected_region = region[regions.key]
        if use_default_region:
            cloudboot_config[DEFAULT_REGION] = selected_region
            rewrite_store(CLOUDBOOT, cloudboot_config)
            set_default_functions_region(selected_region)
    return selected_region


def select_function_runtime(region: str = None):
    runtime_prefix = inquirer.select(message='Select runtime environment', choices=list(map(str, CloudServiceRuntime)),
                                     default=CloudServiceRuntime.PYTHON).execute()
    runtimes = list_runtimes(runtime_prefix, region)
    runtime_choices = runtimes.choices()
    runtime = inquirer.select(message=f'Select {runtime_prefix} version', choices=runtime_choices).execute()
    return runtime[runtimes.key], runtime_prefix


def select_function_trigger(default_region: str):
    trigger: CloudServiceTrigger = inquirer.select(message="Select function trigger",
                                                   choices=list(map(str, CloudServiceTrigger)),
                                                   default=CloudServiceTrigger.HTTP).execute()
    trigger_event = None
    trigger_name = None
    trigger_location = None
    trigger_verified = False
    if trigger in trigger_selector:
        use_existing_resource = inquirer.confirm(message=f'Select an existing {trigger} resource as trigger').execute()
        if use_existing_resource:
            existing_resources = trigger_selector[trigger]['list']()
            existing_resources_choices = existing_resources.choices()
            if not existing_resources.is_empty():
                selected_trigger = inquirer.select(message=f'Select {trigger} trigger',
                                                   choices=existing_resources_choices).execute()
                if 'location' in selected_trigger:
                    trigger_location = selected_trigger['location'].lower()
                if selected_trigger:
                    trigger_name = selected_trigger[existing_resources.key]
                    trigger_verified = True
            else:
                color_print([(ColorCode.WARNING, f'No {trigger} resources available currently!')])
        if not trigger_name or not use_existing_resource:
            trigger_name = trigger_selector[trigger]['new'].execute()
            if trigger == CloudServiceTrigger.FIRESTORE:
                firestore_locations = list_firestore_database_locations()
                locations_choices = firestore_locations.choices()
                default_location_choice = firestore_locations.find_choice(default_region, locations_choices)
                selected_location = inquirer.select(message=f'Select the location for new {trigger}',
                                                    choices=locations_choices,
                                                    default=default_location_choice).execute()
                if selected_location:
                    trigger_location = selected_location[firestore_locations.key]
        if trigger == CloudServiceTrigger.FIRESTORE:
            events = get_functions_event_types(trigger)
            events_choices = events.choices()
            selected_event = inquirer.select(message=f'Select the event type', choices=events_choices,
                                             default=events_choices[0].value).execute()
            if selected_event:
                trigger_event = selected_event[events.key]
    return trigger, trigger_event, trigger_name, trigger_location, trigger_verified


def init_cloud_function():
    cloudboot_config = get_store(CLOUDBOOT)
    color_print([(ColorCode.HIGHLIGHT, '<<<- New Cloud Function ->>>')])
    name = inquirer.text(message='Name', default='my-function').execute()
    selected_region = select_function_region(cloudboot_config)
    selected_runtime, runtime_prefix = select_function_runtime(selected_region)
    trigger, trigger_event, trigger_name, trigger_location, trigger_verified = select_function_trigger(selected_region)
    if not trigger_location:
        trigger_location = selected_region
    template = init_function_sources(name, runtime_prefix, trigger)
    cloud_function_config = CloudFunctionConfig(name, selected_runtime, runtime_prefix)
    cloud_function_config.set_trigger_config(trigger, trigger_name, trigger_location, trigger_verified)
    cloud_function_config.set_trigger_event(trigger_event)
    cloud_function_config.set_region_config(selected_region)
    cloud_function_config.set_entrypoint(template.entrypoint)
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
    deploy_selected_function(function, functions)


def display_available_functions_templates():
    runtime_prefix = inquirer.select(message='Select runtime environment', choices=list(map(str, CloudServiceRuntime)),
                                     default=CloudServiceRuntime.PYTHON).execute()
    list_available_functions_templates(runtime_prefix)
