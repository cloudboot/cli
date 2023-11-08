from InquirerPy import inquirer
from InquirerPy.utils import color_print

from cloudboot.enum.ColorCode import ColorCode
from cloudboot.service.gcloud.auth import valid_gcloud_credentials, get_active_service_account, set_gcloud_credentials


def update_gcloud_credentials():
    creds_file_path = inquirer.text(message='Path to credentials file', default='credentials.json').execute()
    set_gcloud_credentials(creds_file_path)


def ensure_gcloud_credentials():
    new_creds = inquirer.confirm(message='Reset gcloud credentials').execute()
    if new_creds:
        update_gcloud_credentials()
        return
    authorized = valid_gcloud_credentials()
    if authorized:
        color_print([(ColorCode.INFO, 'Found valid credentials!')])
        account = get_active_service_account()
        color_print([(ColorCode.INFO, 'Selected service account: '), (ColorCode.HIGHLIGHT, account)])
        return account
    color_print([(ColorCode.WARNING, 'Could not find valid credentials!')])
    update_gcloud_credentials()
