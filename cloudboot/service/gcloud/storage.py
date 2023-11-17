import json

from cloudboot.consts import GCLOUD_CLI_FLAGS
from cloudboot.model.DataMap import DataMap
from cloudboot.utility.executor import execute

GCLOUD_STORAGE_BUCKETS = 'gcloud storage buckets'


def create_storage_bucket(name: str, location: str = 'asia'):
    bucket = name if name.startswith('gs://') else f'gs://{name}'
    cmd = f'{GCLOUD_STORAGE_BUCKETS} create {bucket}'
    if location:
        cmd = f'{cmd} --location={location}'
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
    bucket = bucket if bucket.startswith('gs://') else f'gs://{bucket}'
    cmd = f'{GCLOUD_STORAGE_BUCKETS} describe {bucket} {GCLOUD_CLI_FLAGS}'
    succeeded, result = execute(cmd)
    if succeeded:
        result = json.loads(result)
        if result['storage_url'] and bucket in result['storage_url']:
            return result
    return False
