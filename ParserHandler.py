import ConfigParser

object_parser = None
environment_parser = None
neural_network_parser = None


def get_environment_cfg():
    global environment_parser
    if environment_parser is None:
        environment_parser = _build_config_parser(url_file_cfg_environment)
    return environment_parser


def get_object_cfg():
    global object_parser
    if object_parser is None:
        object_parser = _build_config_parser(url_file_cfg_object)
    return object_parser


def get_neural_network_cfg():
    global neural_network_parser
    if neural_network_parser is None:
        neural_network_parser = _build_config_parser(url_file_cfg_net_descriptor)
    return neural_network_parser


def _build_config_parser(url_file_cfg):
    config = ConfigParser.RawConfigParser()
    config.read(url_file_cfg)
    return config

default_separator = ','

url_file_cfg_environment = 'config/Environment.properties'
url_file_cfg_object = 'config/Object.properties'
url_file_cfg_net_descriptor = 'config/NetDescriptor2.properties'

property_name_environment_cfg_neural_network_ids = 'neural_networks_ids'
property_name_environment_cfg_name = 'name'
property_name_environment_cfg_frequently_objects = 'frequently_objects'

property_name_object_cfg_name = 'name'

property_name_net_descriptor_environment = 'net.environment'
property_name_net_descriptor_model = 'net.model'
property_name_net_descriptor_mean = 'net.mean'
property_name_net_descriptor_prototype = 'net.prototype'
property_name_net_descriptor_classes = 'net.classes'
property_name_net_descriptor_name = 'net.name'

if __name__ == '__main__':
    a = get_environment_cfg()
    print a.get('1', property_name_environment_cfg_name)
