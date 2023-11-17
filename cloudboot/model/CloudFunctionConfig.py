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
    trigger_event = None
    trigger_resource_verified = False
    region = None

    def __init__(self, name, runtime, runtime_prefix):
        self.name = name
        self.runtime = runtime
        self.runtime_prefix = runtime_prefix

    def set_trigger_config(self, trigger_type: CloudServiceTrigger, trigger_name: str, location: str, verified=False):
        self.trigger_type = trigger_type
        self.trigger_name = trigger_name.lower() if trigger_type == CloudServiceTrigger.FIRESTORE else trigger_name
        self.trigger_resource_verified = verified
        if location:
            self.trigger_location = location.lower()

    def set_trigger_event(self, event):
        self.trigger_event = event

    def set_region_config(self, region: str):
        self.region = f'{region.lower()}'

    def set_entrypoint(self, ep):
        if ep:
            self.entrypoint = ep

    def get_options(self):
        options = f'{self.name} --gen2 --runtime={self.runtime} --region={self.region} --entry-point={self.entrypoint}'
        if not self.trigger_name or self.trigger_type == CloudServiceTrigger.HTTP:
            options = f'{options} --trigger-http'
            options = f'{options} --no-allow-unauthenticated'
        if self.trigger_type == CloudServiceTrigger.FIRESTORE:
            options = f'{options} --trigger-event-filters="type={self.trigger_event},database={self.trigger_name}"'
        elif self.trigger_type == CloudServiceTrigger.PUBSUB:
            options = f'{options} --trigger-topic={self.trigger_name}'
        elif self.trigger_type == CloudServiceTrigger.STORAGE:
            options = f'{options} --trigger-bucket={self.trigger_name}'
        if self.trigger_location and self.trigger_type != CloudServiceTrigger.HTTP:
            options = f'{options} --trigger-location={self.trigger_location}'
        return f'{options} --source={SRC_DIR}/{self.name}'
