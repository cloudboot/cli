import json

import requests

from cloudboot.config import TEMPLATES_REGISTRY_URL
from cloudboot.consts import TEMPLATES
from cloudboot.enum.CloudService import CloudService
from cloudboot.enum.CloudServiceRuntime import CloudServiceRuntime
from cloudboot.enum.CloudServiceTrigger import CloudServiceTrigger
from cloudboot.model.DataMap import DataMap
from cloudboot.model.Template import Template
from cloudboot.utility.store import store_exists, rewrite_store, get_store


def local_template_registry_exists():
    return store_exists(TEMPLATES)


def fetch_templates_registry():
    response = requests.get(TEMPLATES_REGISTRY_URL)
    if not store_exists(TEMPLATES):
        rewrite_store(TEMPLATES, json.loads(response.content))


def get_templates() -> dict:
    if not local_template_registry_exists():
        fetch_templates_registry()
    return get_store(TEMPLATES)


def get_template_config(service: CloudService, runtime: CloudServiceRuntime, trigger: CloudServiceTrigger):
    templates_dict = get_templates()
    if service in templates_dict and runtime in templates_dict[service] and trigger in templates_dict[service][runtime]:
        return Template(**templates_dict[service][runtime][trigger])
    return None


def available_templates(service: CloudService, runtime: CloudServiceRuntime):
    data = DataMap('trigger', 'url')
    templates = get_templates()
    if service in templates.keys() and runtime in templates[service].keys():
        for key, value in templates[service][runtime].items():
            data.push_one(key=key, value={'trigger': key, 'url': value['src']})
    return data
