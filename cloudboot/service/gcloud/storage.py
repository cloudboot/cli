import json

from cloudboot.consts import GCLOUD_CLI_FLAGS
from cloudboot.model.DataMap import DataMap
from cloudboot.utility.executor import execute

GCLOUD_STORAGE_BUCKETS = 'gcloud storage buckets'


def create_storage_bucket(name):
    bucket = f'gs://{name}'
    cmd = f'{GCLOUD_STORAGE_BUCKETS} create {bucket}'
    succeeded, result = execute(cmd)
    if not succeeded:
        return False
    return storage_bucket_exists(bucket)


def list_storage_buckets():
    data = DataMap('storage_url', 'name')
    cmd = f'{GCLOUD_STORAGE_BUCKETS} list {GCLOUD_CLI_FLAGS}'
    succeeded, results = execute(cmd)
    if succeeded:
        results = json.loads(results)
        if len(results):
            data.push_all(results)
    return data


def storage_bucket_exists(bucket):
    cmd = f'{GCLOUD_STORAGE_BUCKETS} describe gs://{bucket} {GCLOUD_CLI_FLAGS}'
    succeeded, result = execute(cmd)
    if succeeded:
        result = json.loads(result)
        if result['name'] and result['name'] == bucket:
            return result['storage_url']
    return False
