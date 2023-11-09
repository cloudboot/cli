from cloudboot.utility.executor import execute

GCLOUD_STORAGE_BUCKETS = 'gcloud storage buckets'


def create_bucket(name):
    bucket = f'gs://{name}'
    cmd = f'{GCLOUD_STORAGE_BUCKETS} create {bucket}'
    succeeded, result = execute(cmd)
    if not succeeded:
        return False
    return bucket_exists(bucket)


def list_buckets():
    cmd = f'{GCLOUD_STORAGE_BUCKETS} list'
    succeeded, results = execute(cmd)
    if not succeeded:
        return []
    results = list(filter(lambda elem: 'name:' in elem, results.strip().split('\n')))
    return [element.replace('name: ', '') for element in results]


def bucket_exists(bucket):
    cmd = f'{GCLOUD_STORAGE_BUCKETS} describe gs://{bucket}'
    succeeded, result = execute(cmd)
    if not succeeded:
        return False
    result = list(filter(lambda elem: 'name:' in elem, result.strip().split('\n')))
    if len(result):
        return result[0].replace('name: ', '')
    return False
