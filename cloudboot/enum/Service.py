from enum import StrEnum


class Service(StrEnum):
    FIRESTORE = 'firestore'
    FUNCTIONS = 'functions'
    PUBSUB = 'pubsub'
    RUN = 'run'
    TOPIC = 'topic'
