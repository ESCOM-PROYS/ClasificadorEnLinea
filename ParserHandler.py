import ConfigParser


def get_environment_cfg():
    return build_config_parser('/config/Objects.properties')


def get_object_cfg():
    return build_config_parser('/config/Environments.properties')


def build_config_parser(urlFileCfg):
    config = ConfigParser.RawConfigParser()
    config.read(urlFileCfg)
    return config

