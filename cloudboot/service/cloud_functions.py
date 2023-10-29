from InquirerPy import inquirer
from InquirerPy.utils import color_print

from cloudboot.config import SRC_DIR
from cloudboot.enum.Common import Trigger, Runtime
from cloudboot.model.CloudFunctionConfig import CloudFunctionConfig
from cloudboot.service.pubsub import topic_exists, create_pubsub_topic
from cloudboot.service.storage import bucket_exists, create_bucket
from cloudboot.utility.downloader import download_template
from cloudboot.utility.executor import execute
from cloudboot.utility.file_manager import extract_zip_file, directory_checksum
from cloudboot.utility.store import retrieve_data, data_exists, store_data

GCLOUD_FUNCTIONS = 'gcloud functions'
CLOUD_FUNCTIONS_STORE = 'cloud_functions'
RUNTIMES_STORE_PREFIX = 'cloud_functions_runtimes'
REGIONS_STORE = 'cloud_functions_regions'


def cache_runtimes(region=None):
    cmd = f'{GCLOUD_FUNCTIONS} runtimes list'
    store_name = RUNTIMES_STORE_PREFIX
    if region:
        cmd = f'{cmd} --region={region}'
        store_name = f'{store_name}_{region}'
    results = execute(cmd).strip().split('\n')
    results.pop()
    prefixes = list(map(str, Runtime))
    runtimes = {prefix: [] for prefix in prefixes}
    while len(results) > 0:
        element = results.pop().split()
        if not len(element):
            continue
        for prefix in prefixes:
            if prefix in element:
                runtimes[prefix].append(element)
                continue
    store_data(store_name, runtimes)


def list_runtimes(runtime_prefix: Runtime, region=None):
    store_name = RUNTIMES_STORE_PREFIX
    if region:
        store_name = f'{store_name}_{region}'
    if not data_exists(store_name):
        cache_runtimes(region)
    return retrieve_data(store_name)[runtime_prefix]


def list_regions():
    if not data_exists(REGIONS_STORE):
        cmd = f'{GCLOUD_FUNCTIONS} regions list --gen2'
        regions = execute(cmd).strip().split('\n').pop()
        store_data(REGIONS_STORE, regions)
    return retrieve_data(REGIONS_STORE)


def set_default_functions_region(region):
    cmd = f'gcloud config set functions/region {region}'
    return execute(cmd)


def init_function_sources(name, runtime: Runtime, trigger: Trigger):
    archive = download_template(runtime, trigger)
    extract_zip_file(archive, '/'.join([SRC_DIR, name]))


def verify_trigger(trigger: Trigger, trigger_name: str, auto_configure=True):
    verified = None
    match trigger:
        case trigger.PUBSUB:
            verified = topic_exists(trigger_name)
        case trigger.STORAGE:
            verified = bucket_exists(trigger_name)
    if verified:
        return verified
    if not auto_configure:
        auto_configure = inquirer.confirm(
            message=f'No such {trigger} exists as {trigger_name}. Create new {trigger}?',
            default=True
        )
    if auto_configure:
        color_print([('yellow', f'Creating new {trigger} : {trigger_name}')])
        match trigger:
            case trigger.PUBSUB:
                verified = create_pubsub_topic(trigger_name)
            case trigger.STORAGE:
                verified = create_bucket(trigger_name)
        return verified
    return False


def deploy_function(function_config):
    function_config = CloudFunctionConfig(**function_config)
    latest_checksum = directory_checksum(f'{SRC_DIR}/{function_config.name}')
    if latest_checksum == function_config.checksum:
        return function_config
    if not function_config.trigger_config_verified:
        result = verify_trigger(function_config.trigger_type, function_config.trigger_name)
        if not result:
            color_print([('#ffc1cc', 'Trigger verification failed! Aborting deployment.')])
            return function_config
        function_config.set_trigger_config(function_config.trigger_type, result)
        function_config.trigger_config_verified = True
    cmd = f'{GCLOUD_FUNCTIONS} deploy {function_config.get_options()}'
    results = execute(cmd).split('\n')
    names = list(filter(lambda line: 'name' in line, results))
    if len(names):
        name = names[0].replace('name: ', '')
        function_config.cloud_resource_name = name
    return function_config


def deploy_functions():
    cloud_functions = retrieve_data(CLOUD_FUNCTIONS_STORE)
    for name, config in cloud_functions.items():
        cloud_functions[name] = deploy_function(config)
    store_data(CLOUD_FUNCTIONS_STORE, cloud_functions)
