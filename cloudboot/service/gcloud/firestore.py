from cloudboot.utility.executor import execute

GCLOUD_FIRESTORE = 'gcloud firestore'


def create_firestore_database(name, location=None):
    cmd = f'{GCLOUD_FIRESTORE} databases create --database={name}'
    if location:
        cmd = f'{cmd}  --location={location}'
    succeeded, result = execute(cmd)
    if not succeeded:
        return None
    return result


def database_exists(database):
    cmd = f'{GCLOUD_FIRESTORE} databases describe --database={database}'
    succeeded, result = execute(cmd)
    if not succeeded:
        return False
    if 'name :' in result:
        result = result.strip().split('\n')
        result = list(filter(lambda line: 'name:' in line, result))
        if len(result):
            return result[0].replace('name: ', '')
    return False


def list_databases():
    cmd = f'{GCLOUD_FIRESTORE} databases list'
    succeeded, result = execute(cmd)
    if not succeeded:
        return []
    result = result.strip().split('\n')
    result = filter(lambda line: 'name:' in line, result)
    return [element.replace('name: ', '') for element in result]
