import re

from cloudboot.utility.executor import execute

GCLOUD_PUBSUB_TOPICS = 'gcloud pubsub topics'


def create_pubsub_topic(name):
    cmd = f'{GCLOUD_PUBSUB_TOPICS} create {name}'
    result = execute(cmd)
    topic = re.search(r'\[(.*)\]', result)
    if topic:
        return topic
    return name


def list_pubsub_topics():
    cmd = f'{GCLOUD_PUBSUB_TOPICS} list'
    return execute(cmd).strip().replace('---\n', '').replace('name: ', '').split()


def topic_exists(topic):
    topics = list_pubsub_topics()
    for element in topics:
        if topic == element or topic == element.split('/')[-1]:
            return element
    return False
