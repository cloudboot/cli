from enum import StrEnum


class CloudResource(StrEnum):
    FIRESTORE = 'firestore'
    FUNCTIONS = 'functions'
    PUBSUB = 'pubsub'
    RUN = 'run'
    STORAGE = 'bucket'


class Trigger(StrEnum):
    FIRESTORE = 'firestore'
    PUBSUB = 'pubsub'
    STORAGE = 'bucket'


class Service(StrEnum):
    CLOUD_FUNCTIONS = 'cloud_functions'
    CLOUD_RUN = 'cloud_run'
