from cloudboot.utility.executor import execute

GCLOUD_FIRESTORE = 'gcloud firestore'


def create_database(name, location):
    cmd = f'{GCLOUD_FIRESTORE} databases create --database={name} --location={location}'
    succeeded, result = execute(cmd)
    if not succeeded:
        return None
    return result
