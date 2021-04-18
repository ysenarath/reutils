import configparser


def load(fp):
    config = configparser.ConfigParser()
    return config.read(fp)


def save(config, fp):
    with open(fp, 'w') as configfile:
        config.write(configfile)
