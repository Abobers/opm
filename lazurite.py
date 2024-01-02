from config import *

class Lazurite:
    versions = ['2.0', '2.1', '2.1.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.6.3', '2.7', '2.7.1']

    @staticmethod
    def version(value = None):
        if value == None:
            return Config.data['lazurite']['version']
        Config.data['lazurite']['version'] = value
        Config.save()

    @staticmethod
    def get(version = None):
        if version == None:
            version = Lazurite.version()
        return Config.data['lazurite'][version]

    @staticmethod
    def set(value, version = None):
        if version == None:
            version = Lazurite.version()
        Config.data['lazurite'][version] = value
        Config.save()
