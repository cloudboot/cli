from cloudboot.model.CloudFunctionConfig import CloudFunctionConfig


def dict_to_cloud_function_config(data) -> CloudFunctionConfig:
    if isinstance(data, CloudFunctionConfig):
        return data
    cloud_function_config = CloudFunctionConfig('', '', '')
    for key, value in data.items():
        setattr(cloud_function_config, key, value)
    return cloud_function_config
