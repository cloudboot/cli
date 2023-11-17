import json

from cloudboot.consts import GCLOUD_CLI_FLAGS
from cloudboot.model.DataMap import DataMap
from cloudboot.utility.executor import execute

GCLOUD_PUBSUB_TOPICS = 'gcloud pubsub topics'


def create_pubsub_topic(name):
    cmd = f'{GCLOUD_PUBSUB_TOPICS} create {name}'
    succeeded, result = execute(cmd)
    if not succeeded:
        return False
    return pubsub_topic_exists(name)


def list_pubsub_topics():
    data = DataMap('name', 'path')
    cmd = f'{GCLOUD_PUBSUB_TOPICS} list {GCLOUD_CLI_FLAGS} {GCLOUD_CLI_FLAGS}'
    succeeded, result = execute(cmd)
    if succeeded:
        result = json.loads(result)
        data.push_all(
            [{
                'name': element['name'].split('/')[-1],
                'path': element['name']
            } for element in result]
        )
    return data


def pubsub_topic_exists(topic):
    cmd = f'{GCLOUD_PUBSUB_TOPICS} describe {topic} {GCLOUD_CLI_FLAGS}'
    succeeded, result = execute(cmd)
    if succeeded:
        result = json.loads(result)
        if len(result):
            return result['name']
    return False
