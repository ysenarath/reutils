import configparser

__all__ = [
    'load',
    'save',
    'dump',
]


def load(fp):
    config = configparser.ConfigParser()
    config.read(fp)
    return config


def save(config, fp):
    with open(fp, 'w') as configfile:
        config.write(configfile)


dump = save
