from cloudboot.enum.Common import Common
from cloudboot.enum.Crud import Crud
from cloudboot.enum import Property
from cloudboot.enum.Service import Service
from cloudboot.utility.executor import execute


def list_locations(service: Service):
    cmd = ' '.join([
        Common.GCLOUD,
        service,
        Property.REGIONS,
        Crud.LIST
    ])
    result = execute(cmd)
    return result
