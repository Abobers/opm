import os
from os.path import abspath, exists, isdir
from command import *

class LazuriteVersion(ExtendedCommand):
    @staticmethod
    def get():
        if Lazurite.version():
            print('Основная версия Lazurite:', Lazurite.version())
        else:
            print(f'Основная версия Lazurite не указана.')

    @staticmethod
    def set(version):
        if version not in Lazurite.versions:
            print('Не удалось выполнить команду.')
            return print(f'Указанная версия Lazurite ({version}) не существует.')
        if not Lazurite.get(version):
            print('Не удалось выполнить команду.')
            return print(f'Отсутствует путь до библиотек для Lazurite {version}.')

        if Lazurite.get(version):
            if Lazurite.version():
                print(f'Основная версия Lazurite изменена с {Lazurite.version()} на {version}')
            else:
                print('Основная версия Lazurite изменена на', version)
            Lazurite.version(version)

    @staticmethod
    def execute(version = None):
        if version:
            LazuriteVersion.set(version)
        else:
            LazuriteVersion.get()

class LazuritePath(ExtendedCommand):
    @staticmethod
    def get(version):
        if version not in Lazurite.versions:
            print('Не удалось выполнить команду.')
            return print(f'Указанная версия Lazurite ({version}) не существует.')

        value = Lazurite.get(version)
        if value:
            print(f'Путь до библиотек для Lazurite {version}: {abspath(value)}.')
        else:
            print(f'Путь до библиотек для Lazurite {version} не указан.')

    @staticmethod
    def set(args: list):
        version = args[0]
        path = ' '.join(args[1:])

        if version not in Lazurite.versions:
            print('Не удалось выполнить команду.')
            return print(f'Причина: Указанная версия Lazurite ({version}) не существует.')
        if not exists(path):
            print('Не удалось выполнить команду.')
            return print(f'Причина: Путь "{abspath(path)}" не существует.')
        if not isdir(path):
            print('Не удалось выполнить команду.')
            return print(f'Причина: Путь "{abspath(path)}" не является папкой.')

        for v in Lazurite.versions:
            if Lazurite.get(v) == path:
                print('Не удалось выполнить команду.')
                return print(f'Причина: Путь "{abspath(path)}" уже установлен для библиотек для Lazurite {v}.')

        if Lazurite.get(version):
            libs = Config.data['libs'][version]
            if libs == {}:
                print('Нет файлов для перемещения.')
            else:
                for lib in Config.data['libs'][Lazurite.version()]:
                    print(f'Перемещение {lib}...')
                    os.rename(Lazurite.get(version) + os.sep + lib + '.lzr', path + os.sep + lib + '.lzr')
                print('Все файлы перемещены.')

        print('Обновление config.json...')
        Lazurite.set(path, version)
        print(f'Путь "{abspath(path)}" установлен для библиотек для Lazurite {version}.')

    @staticmethod
    def delete(version):
        if version not in Lazurite.versions:
            print('Не удалось выполнить команду.')
            return print(f'Причина: Указанная версия Lazurite ({version}) не существует.')
        Lazurite.set(None, version)
        print(f'Путь до Lazurite {version} удалён из config.json')

    @staticmethod
    def execute(args):
        if len(args) == 1:
            LazuritePath.get(args[0])
        elif len(args) == 2:
            LazuritePath.set(args)

class LazuritePaths(Command):
    @staticmethod
    def execute():
        table = PrettyTable()
        table.field_names = ['Lazurite', 'Путь']
        for version in reversed(Lazurite.versions):
            if Lazurite.get(version):
                table.add_row([version, abspath(Lazurite.get(version))])
            else:
                table.add_row([version, 'не указан'])
        print(table)
