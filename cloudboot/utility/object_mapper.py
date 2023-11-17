from cloudboot.model.CloudFunctionConfig import CloudFunctionConfig


def dict_to_cloud_function_config(data) -> CloudFunctionConfig:
    """ Convert a dictionary object into a cloud function configuration instance.

    Maps existing keys and values in the dictionary object and creates a new cloud functions configuration instance.

    Parameters
    -----------
    data: any
        Dictionary object to be mapped. If the data is already an instance of the CloudFunctionConfig class returns
        itself.
    """
    if isinstance(data, CloudFunctionConfig):
        return data
    cloud_function_config = CloudFunctionConfig('', '', '')
    for key, value in data.items():
        setattr(cloud_function_config, key, value)
    return cloud_function_config
