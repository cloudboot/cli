from enum import StrEnum


class Common(StrEnum):
    GCLOUD = 'gcloud'
    CLOUD_RESOURCES = 'cloud_resources'


class Args(StrEnum):
    DATABASE = '--database'
    LOCATION = '--location'
    NAME = '--name'
    REGION = '--region'
    RUNTIME = '--runtime'
    SET_AS_DEFAULT = '--set-as-default'


class Trigger(StrEnum):
    HTTPS = 'https'
    FIRESTORE = 'firestore'
    PUBSUB = 'pubsub'
    STORAGE = 'storage'


class Runtime(StrEnum):
    DOTNET = 'dotnet'
    GO = 'go'
    JAVA = 'java'
    NODEJS = 'nodejs'
    PHP = 'php'
    PYTHON = 'python'
    RUBY = 'ruby'
