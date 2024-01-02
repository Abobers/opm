from config import *
from lazurite import *

class Library:
    @staticmethod
    def libs(version = None):
        if version == None:
            version = Lazurite.version()
        return list(Config.data['libs'][version])

    @staticmethod
    def get(name, version = None):
        if version == None:
            version = Lazurite.version()
        return Config.data['libs'][version][name]

    @staticmethod
    def set(name, value: dict, version = None):
        if version == None:
            version = Lazurite.version()
        Config.data['libs'][version][name] = value
        Config.save()

    @staticmethod
    def delete(name, version = None):
        if version == None:
            version = Lazurite.version()
        del Config.data['libs'][version][name]
        Config.save()
