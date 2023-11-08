import json

import requests

from cloudboot.config import TEMPLATES_REGISTRY_URL
from cloudboot.consts import TEMPLATES
from cloudboot.enum.CloudServiceTrigger import CloudServiceTrigger
from cloudboot.enum.CloudServiceRuntime import CloudServiceRuntime
from cloudboot.enum.CloudService import CloudService
from cloudboot.model.DataMap import DataMap
from cloudboot.model.Template import Template
from cloudboot.utility.store import store_exists, rewrite_store, get_store


def fetch_template_registry():
    response = requests.get(TEMPLATES_REGISTRY_URL)
    if not store_exists(TEMPLATES):
        rewrite_store(TEMPLATES, json.loads(response.content))


def get_templates():
    return get_store(TEMPLATES)


def get_template_config(service: CloudService, runtime: CloudServiceRuntime, trigger: CloudServiceTrigger):
    templates_dict = get_templates()
    if service in templates_dict and runtime in templates_dict[service] and trigger in templates_dict[service][runtime]:
        return Template(**templates_dict[service][runtime][trigger])
    return None


def list_available_templates(service: CloudService, runtime: CloudServiceRuntime):
    data_map = DataMap()
    templates_dict = get_templates()
    if service in templates_dict and runtime in templates_dict[service]:
        for trigger, template_config in templates_dict[service][runtime]:
            data_map.push(trigger, Template(**template_config))
    return data_map
