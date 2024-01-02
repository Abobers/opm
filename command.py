from prettytable import PrettyTable
from config_api import *

class Command:
    @staticmethod
    def execute():
        raise NotImplementedError



class ExtendedCommand(Command):
    @staticmethod
    def get():
        raise NotImplementedError

    @staticmethod
    def set():
        raise NotImplementedError
