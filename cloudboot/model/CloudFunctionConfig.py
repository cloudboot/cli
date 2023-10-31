from cloudboot.config import SRC_DIR
from cloudboot.enum.Common import Runtime, Trigger
from cloudboot.model.Base import Base


class CloudFunctionConfig(Base):
    name: str = ''
    entrypoint: str = 'main'
    runtime_prefix: Runtime = Runtime.PYTHON
    runtime: str = 'python310'
    checksum: str = ''
    cloud_resource_name = ''
    trigger_type: Trigger = Trigger.HTTPS
    trigger_name = None
    trigger_config = None
    trigger_config_verified = False
    region_config = None

    def __init__(self, name, runtime, runtime_prefix):
        self.name = name
        self.runtime = runtime
        self.runtime_prefix = runtime_prefix

    def set_trigger_config(self, trigger_type: Trigger, trigger_name):
        self.trigger_type = trigger_type
        self.trigger_name = trigger_name
        match trigger_type:
            case Trigger.HTTPS:
                self.trigger_config = '--trigger-http'
                self.trigger_config_verified = True
            case Trigger.PUBSUB:
                self.trigger_config = f'--trigger-topic={trigger_name}'
            case Trigger.STORAGE:
                self.trigger_config = f'--trigger-bucket={trigger_name}'

    def set_region_config(self, region):
        self.region_config = f'--region={region}'

    def get_options(self):
        options = f'{self.name} --gen2 --runtime={self.runtime} {self.trigger_config} {self.region_config}'
        return f'{options} --entry-point={self.entrypoint} --source={SRC_DIR}/{self.name}'
