import re

from cloudboot.utility.executor import execute

GCLOUD_PUBSUB_TOPICS = 'gcloud pubsub topics'


def create_pubsub_topic(name):
    cmd = f'{GCLOUD_PUBSUB_TOPICS} create {name}'
    succeeded, result = execute(cmd)
    if not succeeded:
        exit(1)
    topic = re.search(r'\[(.*)\]', result)
    if topic:
        return topic
    return name


def list_pubsub_topics():
    cmd = f'{GCLOUD_PUBSUB_TOPICS} list'
    succeeded, result = execute(cmd)
    if not succeeded:
        return []
    return result.strip().replace('---\n', '').replace('name: ', '').split()


def topic_exists(topic):
    topics = list_pubsub_topics()
    for element in topics:
        if topic == element or topic == element.split('/')[-1]:
            return element
    return False
