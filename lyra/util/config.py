import os

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser


CONVPOOL = 'CONVPOOL'
FULLYCONNECTED = 'FULLYCONNECTED'
COMMON = 'COMMON'


class Config(object):
    def __init__(self, filename, section):
        if not(os.path.exists(filename)):
            raise ValueError("{} does not exist".format(filename))
        parser = ConfigParser()
        parser.read(filename)

        config = parser.items(section)
        config = dict(config)
        #parameters are given in string
        #convert string to float, int or tuple
        for key, item in config.items():
            config[key] = eval(item)

        #set params as attributes
        self.__dict__ = config
