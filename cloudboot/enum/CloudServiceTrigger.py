from enum import StrEnum


class CloudServiceTrigger(StrEnum):
    HTTP = 'http'
    FIRESTORE = 'firestore'
    PUBSUB = 'pubsub'
    STORAGE = 'storage'
