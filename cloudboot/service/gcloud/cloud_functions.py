from InquirerPy import inquirer
from InquirerPy.utils import color_print

from cloudboot.config import SRC_DIR
from cloudboot.enum.CloudService import CloudService
from cloudboot.enum.CloudServiceRuntime import CloudServiceRuntime
from cloudboot.enum.CloudServiceTrigger import CloudServiceTrigger
from cloudboot.enum.ColorCode import ColorCode
from cloudboot.service.core.template import get_template_config
from cloudboot.service.gcloud.pubsub import topic_exists, create_pubsub_topic
from cloudboot.service.gcloud.storage import bucket_exists, create_bucket
from cloudboot.utility.downloader import download_template
from cloudboot.utility.executor import execute
from cloudboot.utility.file_manager import extract_zip_file, directory_checksum
from cloudboot.utility.object_mapper import dict_to_cloud_function_config
from cloudboot.utility.store import get_store, store_exists, rewrite_store

GCLOUD_FUNCTIONS = 'gcloud functions'
RUNTIMES_STORE_PREFIX = 'cloud_functions_runtimes'
REGIONS_STORE = f'{CloudService.CLOUD_FUNCTIONS}_regions'


def cache_runtimes(region=None):
    cmd = f'{GCLOUD_FUNCTIONS} runtimes list'
    store_name = RUNTIMES_STORE_PREFIX
    if region:
        cmd = f'{cmd} --region={region}'
        store_name = f'{store_name}_{region}'
    succeeded, results = execute(cmd)
    if not succeeded:
        exit(1)
    results = results.strip().split('\n')
    del results[0]
    prefixes = list(map(str, CloudServiceRuntime))
    runtimes = {prefix: [] for prefix in prefixes}
    while len(results) > 0:
        element = results.pop().split()
        if not len(element):
            continue
        for prefix in prefixes:
            if prefix in element[0]:
                runtimes[prefix].append(element[0])
                continue
    rewrite_store(store_name, runtimes)


def list_runtimes(runtime_prefix: CloudServiceRuntime, region=None):
    store_name = RUNTIMES_STORE_PREFIX
    if region:
        store_name = f'{store_name}_{region}'
    if not store_exists(store_name):
        cache_runtimes(region)
    return get_store(store_name)[runtime_prefix]


def list_regions():
    if not store_exists(REGIONS_STORE):
        cmd = f'{GCLOUD_FUNCTIONS} regions list --gen2'
        succeeded, regions = execute(cmd)
        if not succeeded:
            exit(1)
        regions = regions.strip().split('\n')
        del regions[0]
        regions = [r.split('/')[-1] for r in regions]
        rewrite_store(REGIONS_STORE, regions)
    return get_store(REGIONS_STORE)


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


def verify_trigger(trigger: CloudServiceTrigger, trigger_name: str, auto_configure=True):
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
        color_print([(ColorCode.HIGHLIGHT, f'Creating new {trigger} : {trigger_name}')])
        match trigger:
            case trigger.PUBSUB:
                verified = create_pubsub_topic(trigger_name)
            case trigger.STORAGE:
                verified = create_bucket(trigger_name)
        return verified
    return False


def deploy_function(function_config):
    function_config = dict_to_cloud_function_config(function_config)
    latest_checksum = directory_checksum(f'{SRC_DIR}/{function_config.name}')
    if latest_checksum == function_config.checksum:
        return function_config
    color_print([(ColorCode.INFO, 'Changes have been detected! Deploying '), (ColorCode.HIGHLIGHT, function_config.name)])
    if not function_config.trigger_config_verified:
        result = verify_trigger(function_config.trigger_type, function_config.trigger_name)
        if not result:
            color_print([(ColorCode.ERROR, '\tTrigger verification failed! Aborting deployment.')])
            return function_config
        function_config.set_trigger_config(function_config.trigger_type, result)
        function_config.trigger_config_verified = True
    cmd = f'{GCLOUD_FUNCTIONS} deploy {function_config.get_options()}'
    succeeded, results = execute(cmd)
    if not succeeded:
        exit(1)
    results = results.split('\n')
    names = list(filter(lambda line: 'name' in line, results))
    if len(names):
        name = names[0].replace('name: ', '')
        function_config.cloud_resource_name = name
        function_config.checksum = latest_checksum
        color_print([(ColorCode.SUCCESS, f'\t{function_config.name} has been deployed successfully!')])
        color_print([('', '\tCloud resource path: '), (ColorCode.HIGHLIGHT, function_config.cloud_resource_name)])
    return function_config


def deploy_functions():
    color_print([(ColorCode.INFO, 'Deploying changes is in progress!')])
    cloud_functions = get_local_functions_list()
    for name, config in cloud_functions.items():
        cloud_functions[name] = deploy_function(config)
    rewrite_store(CloudService.CLOUD_FUNCTIONS, cloud_functions)
    color_print([('', 'Deployment process finished!')])


def list_local_functions():
    color_print([(ColorCode.INFO, 'Functions created using Cloud Bootstrapper:')])
    functions = get_local_functions_list()
    if len(functions):
        for key, element in functions.items():
            element = dict_to_cloud_function_config(element)
            runtime = element.runtime
            color_print([('', '\tname: '), (ColorCode.HIGHLIGHT, f'{key}'), ('', '   runtime: '), (ColorCode.HIGHLIGHT,
                                                                                                   f'{runtime}')])
    else:
        color_print([(ColorCode.INFO, 'Could not find any cloud function locally!')])


def get_local_functions_list():
    return get_store(CloudService.CLOUD_FUNCTIONS)
