import os
from os.path import abspath, exists, isdir
import requests
import json
from command import *

class LibraryFunctions:
    @staticmethod
    def config(name):
        value = requests.get(f'https://github.com/Abobers/lazurite-modules/blob/main/{name}/config.json')
        if value.status_code == 200:
            value = value.json()['payload']['blob']['rawLines']
            value = json.loads('\n'.join(value))
            return {'result': True, 'value': value}
        else:
            return {'result': False, 'value': value.status_code}

    @staticmethod
    def install(name):
        value = requests.get(f'https://github.com/Abobers/lazurite-modules/blob/main/{name}/{Lazurite.version()}.lzr')
        if value.status_code == 200:
            value = '\n'.join(value.json()['payload']['blob']['rawLines'])
            return {'result': True, 'value': value}
        else:
            return {'result': False, 'value': value.status_code}

    @staticmethod
    def check():
        if not Lazurite.version():
            return {'result': False, 'value': 'Основная версия Lazurite не указана.'}
        if Lazurite.version() not in Lazurite.versions:
            return {'result': False, 'value': f'Lazurite {Lazurite.version()} не существует.'}
        if not Lazurite.get():
            return {'result': False, 'value': f'Путь до библиотек для Lazurite {Lazurite.version()} не указан.'}
        return {'result': True, 'value': None}



class LibraryInstall(Command):
    @staticmethod
    def execute(args: list):
        name = ' '.join(args)

        config = LibraryFunctions.check()
        if not config['result']:
            print('Не удалось выполнить команду.')
            return print('Причина:', config['value'])

        if name in Library.libs():
            print('Не удалось выполнить команду.')
            return print(f'Причина: Библиотека "{name}" уже установлена.')

        config = LibraryFunctions.config(name)
        if not config['result']:
            print('Не удалось выполнить команду.')
            if config['value'] == 404:
                return print(f'Причина: Библиотека "{name}" не существует.')
            return print(f"Причина: Ошибка {config['value']}.")

        config = config['value']
        if Lazurite.version() not in config['lazurite']:
            print('Не удалось выполнить команду.')
            print(f'Причина: Библиотека "{name}" не совместима с Lazurite', Lazurite.version())
            return print('Совместимые версии Lazurite:', ', '.join(config['lazurite']))

        path = Lazurite.get()
        if not exists(path):
            print(f'Папка "{abspath(path)}" не существует')
            os.mkdir(path)
            print(f'Папка "{abspath(path)}" создана')

        value = LibraryFunctions.install(name)
        if not value['result']:
            print('Не удалось выполнить команду.')
            return print(f"Причина: Ошибка {config['value']}.")
        value = value['value']

        path += os.sep + name + '.lzr'
        with open(path, 'w') as file:
            file.write(value)
        print(f'Файл "{abspath(path)}" создан')

        print('Обновление config.json...')
        Library.set(name, {'author': config['author'], 'version': config['version']})
        print(f'Библиотека "{name}" ({config["version"]}) успешно установлена.')



class LibraryDelete(Command):
    @staticmethod
    def execute(args: list):
        name = ' '.join(args)

        config = LibraryFunctions.check()
        if not config['result']:
            print('Не удалось выполнить команду.')
            return print('Причина:', config['value'])

        if name not in Library.libs():
            print('Не удалось выполнить команду.')
            return print(f'Библиотека "{name}" не установлена.')

        path = Lazurite.get()
        if not exists(path):
            print('Не удалось выполнить команду.')
            return print(f'Причина: Папка "{abspath(path)}" не существует.')

        path += os.sep + name + '.lzr'
        if exists(path):
            os.remove(path)
            print(f'Файл "{abspath(path)}" удалён')
        else:
            print(f'Файл "{abspath(path)}" не существует')

        print('Обновление config.json...')
        Library.delete(name)
        print(f'Библиотека "{name}" успешно удалена.')



class LibraryUpdate(Command):
    @staticmethod
    def execute(args: list):
        name = ' '.join(args)

        config = LibraryFunctions.check()
        if not config['result']:
            print('Не удалось выполнить команду.')
            return print('Причина:', config['value'])

        if name not in Library.libs():
            print('Не удалось выполнить команду.')
            return print(f'Причина: Библиотека "{name}" не установлена.')

        config = LibraryFunctions.config(name)
        if not config['result']:
            print('Не удалось выполнить команду.')
            if config['value'] == 404:
                return print(f'Причина: Библиотека "{name}" не существует.')
            return print(f"Причина: Ошибка {config['value']}.")

        config = config['value']
        if Lazurite.version() not in config['lazurite']:
            print('Не удалось выполнить команду.')
            print(f'Причина: Библиотека "{name}" не совместима с Lazurite', Lazurite.version())
            return print('Совместимые версии Lazurite:', ', '.join(config['lazurite']))

        path = Lazurite.get()
        if not isdir(path):
            print('Не удалось выполнить команду.')
            return print(f'Причина: Папка "{abspath(path)}" не существует.')

        path += os.sep + name + '.lzr'
        if not exists(path):
            print('Не удалось выполнить команду.')
            return print(f'Причина: Файл "{abspath(path)}" не существует.')

        if Library.get(name)['version'] == config['version']:
            return print(f'Библиотека "{name}" уже обновлена до последней версии.')

        print(f'Обновление {name}...')
        value = LibraryFunctions.install(name)
        if not value['result']:
            print('Не удалось выполнить команду.')
            return print(f"Причина: Ошибка {config['value']}.")
        value = value['value']

        with open(path, 'w') as file:
            file.write(value)
        print(f'Файл "{abspath(path)}" изменён')

        print('Обновление config.json...')
        old_version = Library.get(name)['version']
        Library.set(name, {'author': config['author'], 'version': config['version']})
        print(f'Обновление библиотеки "{name}" с версии {old_version} до {config["version"]} завершено.')

class LibraryUpdateAll(Command):
    @staticmethod
    def execute():
        config = LibraryFunctions.check()
        if not config['result']:
            print('Не удалось выполнить команду.')
            return print('Причина:', config['value'])

        libs = Config.data['libs'][Lazurite.version()]
        if libs == {}:
            return print('Ни одна библиотека не установлена.')

        for lib in libs:
            config = LibraryFunctions.config(lib)
            if config['result']:
                config = config['value']
                if config['version'] != libs[lib]['version']:
                    LibraryUpdate.execute([lib])
        print('Все библиотеки обновлены до последних версий.')

class LibraryList(Command):
    @staticmethod
    def execute():
        config = LibraryFunctions.check()
        if not config['result']:
            print('Не удалось выполнить команду.')
            return print('Причина:', config['value'])

        libs = Config.data['libs'][Lazurite.version()]
        if libs == {}:
            return print('Ни одна библиотека не установлена.')

        table = PrettyTable()
        table.field_names = ['Библиотека', 'Версия', 'Автор']
        for lib in Config.data['libs'][Lazurite.version()]:
            table.add_row([lib, libs[lib]['version'], libs[lib]['author']])
        print(table)

class LibraryOutdated(Command):
    @staticmethod
    def execute():
        config = LibraryFunctions.check()
        if not config['result']:
            print('Не удалось выполнить команду.')
            return print('Причина:', config['value'])

        libs = Config.data['libs'][Lazurite.version()]
        if libs == {}:
            return print('Ни одна библиотека не установлена.')

        count = 0
        table = PrettyTable()
        table.field_names = ['Библиотека', 'Версия', 'Актуальная версия']

        for lib in libs:
            config = LibraryFunctions.config(lib)
            if config['result']:
                config = config['value']
                if config['version'] != libs[lib]['version']:
                    table.add_row([lib, libs[lib]['version'], config['version']])
                    count += 1
            else:
                print(f'Не удалось загрузить библиотеку "{lib}". Ошибка: {config["result"]}')

        if count:
            print(f'Список устаревших библиотек ({count}):')
            print(table)
        else:
            print('Все библиотеки обновлены до последней версии.')
                
            

class LibraryInfo(Command):
    @staticmethod
    def execute(args: list):
        name = ' '.join(args)

        config = LibraryFunctions.check()
        if not config['result']:
            print('Не удалось выполнить команду.')
            return print('Причина:', config['value'])

        if name not in Library.libs():
            print('Не удалось выполнить команду.')
            return print(f'Причина: Библиотека "{name}" не установлена.')

        lib = Library.get(name)
        print('Название:', name)
        print('Версия:', lib['version'])
        print('Автор:', lib['author'])
