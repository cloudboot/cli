from cloudboot.enum.CloudResource import Resource
from cloudboot.enum.Common import Common, Args
from cloudboot.enum.Crud import Crud
from cloudboot.enum.Property import Property
from cloudboot.utility.executor import execute


def create_database(name, location):
    cmd = ' '.join([
        Common.GCLOUD,
        Resource.FIRESTORE,
        Property.DATABASES,
        Crud.CREATE,
        f'{Args.DATABASE}={name}',
        f'{Args.LOCATION}={location}'
    ])
    return execute(cmd)
