import configparser

_CONFIG = None


def init_config(config_file):
    global _CONFIG
    if _CONFIG is not None:
        raise Exception('config is set already')
    _CONFIG = configparser.ConfigParser()
    _CONFIG.read(config_file)
    return _CONFIG


def get_config():
    return _CONFIG
