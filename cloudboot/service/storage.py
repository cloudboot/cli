from cloudboot.utility.executor import execute

GCLOUD_STORAGE_BUCKETS = 'gcloud storage buckets'


def create_bucket(name):
    bucket = f'gs://{name}'
    cmd = f'{GCLOUD_STORAGE_BUCKETS} create {bucket}'
    execute(cmd)
    return bucket_exists(bucket)


def list_buckets():
    cmd = f'{GCLOUD_STORAGE_BUCKETS} list'
    results = list(filter(lambda elem: 'name' in elem, execute(cmd).strip().split('\n')))
    return [element.replace('name: ', '') for element in results]


def bucket_exists(bucket):
    for element in list_buckets():
        if bucket == element:
            return f'gs://{element}'
    return False
