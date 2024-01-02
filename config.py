import json

class Config:
    @staticmethod
    def load():
        with open('config.json') as file:
            Config.data = json.load(file)

    @staticmethod
    def save():
        with open('config.json', 'w') as file:
            json.dump(Config.data, file, indent = 4)
        Config.load()
