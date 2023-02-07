import re
from datetime import datetime
from pathlib import Path

ABOUT_BOT = '''
The bot accepts commands:

"hello", replies to the console "How can I help you?"
"add ...". With this command, the bot saves a new contact in memory (in the dictionary, for example). Instead of ... the user enters the name and phone number, necessarily with a space.
"change ..." With this command, the bot stores the new phone number of the existing contact in memory. Instead of ..., the user enters the name and phone number in the format +XXXXXXXXXXXX, with a space.
"phone ...." With this command, the bot outputs the phone number for the specified contact to the console. Instead of ... the user enters the name of the contact whose number should be displayed.
"show all". With this command, the bot outputs all saved contacts with phone numbers to the console.
"good bye", "close", "exit" by any of these commands, the bot ends its work after outputting "Good bye!" to the console.
'''
FILENAME = 'phone_book'
phone_book = {}

def main():
    read_files()
    while True:
        parser(input('enter comand: '))


def get_path():
    dir_file = __file__.split('/')[:-1]
    dir_file = Path('/'.join(dir_file)) / 'data'
    return dir_file


def read_files():
    with open(get_path() / FILENAME) as cf:
        phone_book_str = cf.readlines()
    make_phone_book(phone_book_str)


def make_phone_book(phone_book_str):
    for i in phone_book_str:
        k, v = i[:-1].split(' - ')
        phone_book[k] = v.split()


def write_files(phone_book):
    fileneme = FILENAME + '_v_' + str(datetime.now())
    with open(get_path() / fileneme, 'w') as cf:
        for k, v in phone_book.items():
            cf.write(f'{k} - ')
            for i in v:
                cf.write(f'{i} ')
            cf.write('\n')
    with open(get_path() / FILENAME, 'w') as cf:
        for k, v in phone_book.items():
            cf.write(f'{k} - ')
            for i in v:
                cf.write(f'{i} ')
            cf.write('\n')
    exit(0)


def check_phone_number(numb):
    return re.search('[+]?\d{10,12}', numb)



def input_error(parser):
    def inner(command):
        try:
            command = command.lower().split()
            if command[0].lower() in ['change', 'phone']:
                if command[1] not in phone_book:
                    raise KeyError
            elif command[0].lower() in ['change', 'add']:
                if not check_phone_number(command[2]):
                    raise ValueError
            parser(command)
        except IndexError:
            print(ABOUT_BOT)
        except ValueError:
            print(ValueError("Check name and phone please\nuse form +XXXXXXXXXXXX"))
        except KeyError:
            print(KeyError('Check user name'))
    return inner


def command_parser(command):
    if command[0] in ["close", "exit"]:
        return 'exit'
    elif command[0] == "good" and command[1] == "bye":
        return 'exit'
    elif command[0] == 'hello':
        return 'hello'
    elif command[0] == 'show' and command[1] == 'all':
        return 'show all'
    elif command[0] in ['add', 'change']:
        return 'add'
    elif command[0] == 'phone':
        return 'phone'
    else:
        print('Not a valid command')
        print(ABOUT_BOT)


@input_error
def parser(command):
    command_type = command_parser(command)
    if command_type == 'exit':
        write_files(phone_book)
    elif command_type == 'hello':
        print("How can I help you?")
    elif command_type == 'show all':
        for k, v in phone_book.items():
            print(k.capitalize() + ':', end=' ')
            for i in v:
                print(i, end=' ')
            print()
    if command_type == 'add':
        phone_book.setdefault(command[1], []).append(command[2])
    elif command_type == 'phone':
        print(command[1].capitalize() + ':', end=' ')
        for i in phone_book[command[1]]:
            print(i, end=' ')
        print()


if __name__ == '__main__':
    main()

