from cloudboot.config import SRC_DIR
from cloudboot.enum.CloudServiceRuntime import CloudServiceRuntime
from cloudboot.enum.CloudServiceTrigger import CloudServiceTrigger
from cloudboot.model.Base import Base


class CloudFunctionConfig(Base):
    name: str = ''
    entrypoint: str = 'main'
    runtime_prefix: CloudServiceRuntime = CloudServiceRuntime.PYTHON
    runtime: str = 'python310'
    checksum: str = ''
    cloud_resource_name = ''
    trigger_type: CloudServiceTrigger = CloudServiceTrigger.HTTP
    trigger_name = None
    trigger_location = None
    trigger_config = None
    trigger_event = None
    trigger_config_verified = False
    region_config = None

    def __init__(self, name, runtime, runtime_prefix):
        self.name = name
        self.runtime = runtime
        self.runtime_prefix = runtime_prefix

    def set_trigger_config(self, trigger_type: CloudServiceTrigger, trigger_name):
        self.trigger_type = trigger_type
        self.trigger_name = trigger_name
        match trigger_type:
            case CloudServiceTrigger.HTTP:
                self.trigger_config = '--trigger-http'
                self.trigger_config_verified = True
            case CloudServiceTrigger.PUBSUB:
                self.trigger_config = f'--trigger-topic={trigger_name}'
            case CloudServiceTrigger.STORAGE:
                self.trigger_config = f'--trigger-bucket={trigger_name}'
            case CloudServiceTrigger.FIRESTORE:
                self.trigger_config = f'--trigger-resource="{trigger_name}"'

    def set_trigger_event(self, event):
        self.trigger_event = f'--trigger-event={event}'

    def set_region_config(self, region):
        self.region_config = f'--region={region}'

    def get_options(self):
        options = f'{self.name} --gen2 --runtime={self.runtime} {self.trigger_config} {self.region_config}'
        return f'{options} --entry-point={self.entrypoint} --source={SRC_DIR}/{self.name}'
