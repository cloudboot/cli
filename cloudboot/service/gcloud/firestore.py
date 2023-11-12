import json

from cloudboot.consts import GCLOUD_CLI_FLAGS
from cloudboot.enum.CloudServiceTrigger import CloudServiceTrigger
from cloudboot.model.DataMap import DataMap
from cloudboot.utility.executor import execute
from cloudboot.utility.store import store_exists, get_store, rewrite_store

GCLOUD_FIRESTORE = 'gcloud firestore'
FIRESTORE_LOCATIONS_STORE = f'{CloudServiceTrigger.FIRESTORE}_locations'


def create_firestore_database(name, location):
    cmd = f'{GCLOUD_FIRESTORE} databases create --database={name.lower()} --location={location}'
    succeeded, result = execute(cmd)
    if succeeded:
        return firestore_database_exists(name)
    return None


def firestore_database_exists(database):
    cmd = f'{GCLOUD_FIRESTORE} databases describe --database={database.lower()} {GCLOUD_CLI_FLAGS}'
    succeeded, result = execute(cmd)
    if succeeded:
        result = json.loads(result)
        return {
            'name': result['name'],
            'location': result['locationId']
        }
    return False


def list_firestore_databases():
    data = DataMap('name', 'location')
    cmd = f'{GCLOUD_FIRESTORE} databases list {GCLOUD_CLI_FLAGS}'
    succeeded, result = execute(cmd)
    if not succeeded:
        return data
    result = json.loads(result)
    elements = []
    for element in result:
        elements.append(
            {
                'name': element['name'].split('/')[-1],
                'location': element['locationId']
            }
        )
    data.push_all(elements)
    return data


def list_firestore_database_locations():
    data = DataMap('locationId', 'displayName')
    if store_exists(FIRESTORE_LOCATIONS_STORE):
        data.push_all(get_store(FIRESTORE_LOCATIONS_STORE))
        return data
    cmd = f'{GCLOUD_FIRESTORE} locations list {GCLOUD_CLI_FLAGS}'
    succeeded, result = execute(cmd)
    if succeeded:
        result = json.loads(result)
        if len(result):
            data.push_all(result)
        rewrite_store(FIRESTORE_LOCATIONS_STORE, result)
    return data
