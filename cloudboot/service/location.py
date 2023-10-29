from cloudboot.enum.Common import Common
from cloudboot.enum.Crud import Crud
from cloudboot.enum.Property import Property
from cloudboot.enum.CloudResource import CloudResource
from cloudboot.utility.executor import execute


def list_locations(cloud_resource: CloudResource):
    cmd = ' '.join([
        Common.GCLOUD,
        cloud_resource,
        Property.REGIONS,
        Crud.LIST
    ])
    result = execute(cmd)
    return result
