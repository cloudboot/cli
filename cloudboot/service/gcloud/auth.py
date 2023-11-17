from cloudboot.utility.executor import execute

GCLOUD_AUTH = 'gcloud auth'


def valid_gcloud_credentials():
    cmd = f'{GCLOUD_AUTH} list'
    succeeded, result = execute(cmd)
    if not succeeded:
        exit(1)
    return 'No credentialed accounts' not in result


def set_gcloud_credentials(key_file: str):
    cmd = f'{GCLOUD_AUTH} login --cred-file={key_file}'
    succeeded, result = execute(cmd)
    if not succeeded:
        exit(1)
    return result


def get_active_service_account():
    cmd = f'{GCLOUD_AUTH} list --filter=status:ACTIVE --format="value(account)"'
    succeeded, result = execute(cmd)
    if not succeeded:
        exit(1)
    return result
