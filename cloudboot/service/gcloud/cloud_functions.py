import json

from InquirerPy import inquirer
from InquirerPy.utils import color_print

from cloudboot.config import SRC_DIR
from cloudboot.consts import GCLOUD_CLI_FLAGS
from cloudboot.enum.CloudService import CloudService
from cloudboot.enum.CloudServiceRuntime import CloudServiceRuntime
from cloudboot.enum.CloudServiceTrigger import CloudServiceTrigger
from cloudboot.enum.ColorCode import ColorCode
from cloudboot.model.DataMap import DataMap
from cloudboot.service.core.template import get_template_config, available_templates
from cloudboot.service.gcloud.firestore import create_firestore_database, firestore_database_exists
from cloudboot.service.gcloud.pubsub import pubsub_topic_exists, create_pubsub_topic
from cloudboot.service.gcloud.storage import storage_bucket_exists, create_storage_bucket
from cloudboot.utility.downloader import download_template
from cloudboot.utility.executor import execute
from cloudboot.utility.file_manager import extract_zip_file, directory_checksum
from cloudboot.utility.object_mapper import dict_to_cloud_function_config
from cloudboot.utility.store import get_store, store_exists, rewrite_store

GCLOUD_FUNCTIONS = 'gcloud functions'
RUNTIMES_STORE_PREFIX = 'cloud_functions_runtimes'
REGIONS_STORE = f'{CloudService.CLOUD_FUNCTIONS}_regions'
TRIGGER_EVENTS_STORE = f'{CloudService.CLOUD_FUNCTIONS}_trigger_events'


def cloud_function_exists(name: str, region=None):
    cmd = f'{GCLOUD_FUNCTIONS} describe {name} {GCLOUD_CLI_FLAGS}'
    if region:
        cmd = f'{cmd} --region={region}'
    succeeded, result = execute(cmd)
    if succeeded:
        return json.loads(result)
    return False


def list_runtimes(runtime_prefix: CloudServiceRuntime, region=None):
    data = DataMap('name', 'stage')
    cmd = f'{GCLOUD_FUNCTIONS} runtimes list'
    store_name = RUNTIMES_STORE_PREFIX
    store_data = []
    if region:
        cmd = f'{cmd} --region={region}'
        store_name = f'{store_name}_{region}'
    if store_exists(store_name):
        store_data = get_store(store_name)
    else:
        cmd = f'{cmd} {GCLOUD_CLI_FLAGS}'
        succeeded, result = execute(cmd)
        if succeeded:
            store_data = json.loads(result)
            rewrite_store(store_name, store_data)
    selection = []
    for runtime in store_data:
        if 'GEN_2' in runtime['environments'] and runtime_prefix in runtime['name']:
            selection.append(runtime)
    data.push_all(selection)
    return data


def list_regions():
    data = DataMap('locationId', 'displayName')
    if store_exists(REGIONS_STORE):
        regions = get_store(REGIONS_STORE)
        data.push_all(regions)
    cmd = f'{GCLOUD_FUNCTIONS} regions list --gen2 {GCLOUD_CLI_FLAGS}'
    succeeded, regions = execute(cmd)
    if succeeded:
        regions = json.loads(regions)
        data.push_all(regions)
        rewrite_store(REGIONS_STORE, regions)
    return data


def set_default_functions_region(region):
    cmd = f'gcloud config set functions/region {region}'
    succeeded, result = execute(cmd)
    if not succeeded:
        exit(1)
    return result


def init_function_sources(name, runtime_prefix: CloudServiceRuntime, trigger: CloudServiceTrigger):
    template_config = get_template_config(CloudService.CLOUD_FUNCTIONS, runtime_prefix, trigger)
    archive = download_template(template_config)
    extract_zip_file(archive, '/'.join([SRC_DIR, name]), template_config.name)
    return template_config


def verify_trigger(trigger: CloudServiceTrigger, trigger_name: str, location: str = None, auto_configure=True):
    """Verify Cloud resource availability

    Verifies or creates Cloud resource which represents the Cloud function's trigger.

    Parameters
    -----------------------
    trigger: str
        Cloud resource type.
    trigger_name: str
        Name of the cloud resource.
    location:
        Location/region where Cloud resource should be.
    auto_configure:
        Optional, If enabled this method will create the resource if it doesn't exist.
    """
    verified = None
    match trigger:
        case CloudServiceTrigger.FIRESTORE:
            verified = firestore_database_exists(trigger_name)
        case CloudServiceTrigger.PUBSUB:
            verified = pubsub_topic_exists(trigger_name)
        case CloudServiceTrigger.STORAGE:
            verified = storage_bucket_exists(trigger_name)
        case CloudServiceTrigger.HTTP:
            verified = True
    if verified:
        return verified
    if not auto_configure:
        auto_configure = inquirer.confirm(
            message=f'No such {trigger} exists as {trigger_name}. Create new {trigger}?',
            default=True
        ).execute()
    if auto_configure:
        color_print([(ColorCode.HIGHLIGHT, f'Creating new {trigger} : {trigger_name}')])
        match trigger:
            case CloudServiceTrigger.PUBSUB:
                verified = create_pubsub_topic(trigger_name)
            case CloudServiceTrigger.STORAGE:
                verified = create_storage_bucket(trigger_name, location)
            case CloudServiceTrigger.FIRESTORE:
                verified = create_firestore_database(trigger_name, location)
        return verified
    return False


def deploy_function(function_config):
    """Deploy a Cloud Function

    Deploys or creates a Cloud function from locally available sources. Trigger resources will be created before the
    function deployment automatically if they don't exist.

    Parameters
    -----------------------
    function_config: dict
        Cloud function configuration in dictionary form.
    """
    function_config = dict_to_cloud_function_config(function_config)
    latest_checksum = directory_checksum(f'{SRC_DIR}/{function_config.name}')
    if latest_checksum == function_config.checksum:
        return function_config
    color_print(
        [(ColorCode.INFO, 'Changes have been detected! Deploying '), (ColorCode.HIGHLIGHT, function_config.name)])
    if not function_config.trigger_resource_verified or function_config.trigger_type != CloudServiceTrigger.HTTP:
        result = verify_trigger(function_config.trigger_type, function_config.trigger_name,
                                function_config.trigger_location)
        if not result:
            color_print([(ColorCode.ERROR, 'Trigger verification failed! Aborting deployment.')])
            return function_config
        function_config.trigger_resource_verified = True
    cmd = f'{GCLOUD_FUNCTIONS} deploy {function_config.get_options()} {GCLOUD_CLI_FLAGS}'
    succeeded, result = execute(cmd)
    if succeeded:
        result = cloud_function_exists(function_config.name, function_config.region)
        if not result:
            color_print([(ColorCode.WARNING, 'Could not save function metadata. Please try again later!')])
            return function_config
        function_config.checksum = latest_checksum
        function_config.cloud_resource_name = result['name']
        color_print([(ColorCode.SUCCESS, f'{function_config.name} has been deployed successfully!')])
        color_print([('', 'Cloud resource path: '), (ColorCode.HIGHLIGHT, function_config.cloud_resource_name)])
    else:
        color_print([(ColorCode.ERROR, f'Failed to deploy cloud function {function_config.name}')])
    return function_config


def deploy_functions():
    cloud_functions = get_local_functions_list()
    for name, config in cloud_functions.items():
        cloud_functions[name] = deploy_function(config).__dict__
    rewrite_store(CloudService.CLOUD_FUNCTIONS, cloud_functions)


def deploy_selected_function(selected_config, cloud_functions=None):
    """Select and deploy a locally created function

    Deploys selected Cloud function from the local functions sources. Checksum of the sources and the CLoud resource
    name will be saved on a successful deployment.

    Parameters
    -----------------------
    selected_config: dict
        Selected Cloud function configuration in dictionary form.
    cloud_functions: dict
        Optional, Local Cloud functions registry.
    """
    if not cloud_functions:
        cloud_functions = get_local_functions_list()
    result = deploy_function(selected_config)
    if result:
        cloud_functions[result.name] = result.__dict__
        rewrite_store(CloudService.CLOUD_FUNCTIONS, cloud_functions)
        color_print([('', 'Deployment process finished!')])


def list_local_functions():
    """List local configurations

    Prints the list of Cloud functions created with CLoud bootstrapper.
    """
    functions = get_local_functions_list()
    if len(functions):
        color_print([(ColorCode.INFO, 'Functions created using Cloud Bootstrapper:')])
        for key, element in functions.items():
            element = dict_to_cloud_function_config(element)
            runtime = element.runtime
            color_print([('', '\tname: '), (ColorCode.HIGHLIGHT, f'{key}'), ('', '   runtime: '), (ColorCode.HIGHLIGHT,
                                                                                                   f'{runtime}')])
    else:
        color_print([(ColorCode.INFO, 'Local cloud function directory is empty!')])


def get_local_functions_list():
    """Get local configurations

    Reloads and returns locally stored json data on Cloud functions created with CLoud bootstrapper.
    """
    return get_store(CloudService.CLOUD_FUNCTIONS) if store_exists(CloudService.CLOUD_FUNCTIONS) else {}


def get_functions_event_types(resource: CloudServiceTrigger):
    """Fetch available event types

    Retrieves available event types for triggering a Cloud function using a cloud resource like pubsub,
    firestore database or a storage bucket.

    Parameters
    -----------------------
    resource: str
        Selected resource type. i.e. firestore
    """
    events = DataMap('name', 'description')
    store_name = f'{TRIGGER_EVENTS_STORE}-{resource}'
    if store_exists(store_name):
        stored = get_store(store_name)
        events.push_all(stored)
    if events.is_empty():
        cmd = f'{GCLOUD_FUNCTIONS} event-types list --gen2 {GCLOUD_CLI_FLAGS}'
        succeeded, result = execute(cmd)
        if succeeded:
            result = json.loads(result)
            result = list(filter(lambda elem: resource in elem['name'], result))
            events.push_all(result)
            rewrite_store(store_name, result)
    return events


def list_available_functions_templates(runtime: CloudServiceRuntime):
    """List remote templates

    Prints references of remote Cloud functions templates for a given programming language to the console.

    Parameters
    -----------------------
    runtime: str
        Selected runtime prefix. i.e. python
    """
    templates = available_templates(CloudService.CLOUD_FUNCTIONS, runtime)
    if templates.is_empty():
        color_print([(ColorCode.WARNING, f'Could not find any template for the provided runtime {runtime}')])
        exit(0)
    for key in templates.keys:
        color_print([(ColorCode.HIGHLIGHT, f'{key}: '), (ColorCode.INFO, templates.map[key][templates.display_name])])
