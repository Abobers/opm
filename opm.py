from os import system
from pyperclip import paste
from lazurite_commands import *
from lib_commands import *
from help_commands import *



print('=================================='.center(80))
print('Other package manager for Lazurite'.center(80))
print('=================================='.center(80))
print()

def lazurite_argument(value):
    if value in ['last', 'latest']:
        return Lazurite.versions[-1]
    elif value in ['prelast', 'prelatest']:
        return Lazurite.versions[-2]
    elif value in ['this', 'current']:
        if Lazurite.version():
            return Lazurite.version()
        else:
            return 'null'
    return value

Config.load()
system('title opm 1.2')
def read_command(text):
    Config.load()
    cmd = text.split()
    command = cmd[0]
    args = cmd[1:]

    if command == 'lazurite':
        if len(args) == 1:
            if args[0] == 'version':
                LazuriteVersion.execute()
            else:
                print('Команда указана неверно.')
                print('Возможно, вы имели ввиду: lazurite version')
        elif len(args) == 2:
            if args[0] == 'version':
                args[1] = lazurite_argument(args[1])
                LazuriteVersion.execute(args[1])
            else:
                print('Команда указана неверно.')
                print('Возможно, вы имели ввиду: lazurite version <version>')
        else:
            print('Команда указана неверно.')
            print('Возможно, вы имели ввиду:')
            print('1. lazurite version')
            print('2. lazurite version <version>')

    elif command == 'path':
        if len(args) > 0:
            args[0] = lazurite_argument(args[0])
            LazuritePath.execute(args)
        else:
            print('Команда указана неверно.')
            print('Возможно, вы имели ввиду:')
            print('1. path <version>')
            print('2. path <version> <path>')
            print('3. paths')

    elif command == 'paths':
        LazuritePaths.execute()

    elif command in ['list', 'libs']:
        LibraryList.execute()

    elif command == 'outdated':
        LibraryOutdated.execute()

    elif command == 'info':
        if len(args) > 0:
            LibraryInfo.execute(args)
        else:
            print('Команда указана неверно.')
            print('Используйте: info <name>')

    elif command == 'install':
        if len(args) > 0:
            LibraryInstall.execute(args)
        else:
            print('Команда указана неверно.')
            print('Используйте: install <name>')

    elif command == 'update':
        if len(args) > 0:
            LibraryUpdate.execute(args)
        else:
            print('Команда указана неверно.')
            print('Используйте: update <name>')

    elif command == 'updateall':
        if len(args) == 0:
            LibraryUpdateAll.execute()
        else:
            print('Команда указана неверно.')
            print('Используйте: updateall')

    elif command in ['delete', 'uninstall', 'remove']:
        if len(args) > 0:
            LibraryDelete.execute(args)
        else:
            print('Команда указана неверно.')
            print('Используйте: delete <name>')

    elif command == 'help':
        if len(args) == 0:
            HelpHelp.execute()
        else:
            print('Команда указана неверно.')
            print('Используйте: help')

    elif command == 'title':
        if len(args) > 0:
            system('title ' + ' '.join(args))
        else:
            print('Команда указана неверно.')
            print('Используйте: title <text>')

    elif command == 'clear':
        system('cls')

    else:
        print(f'Команда "{text}" не существует.')
    print()

while True:
    Config.load()
    text = input()
    if text.replace(' ', '') != '':
        read_command(text)
    Config.load()
