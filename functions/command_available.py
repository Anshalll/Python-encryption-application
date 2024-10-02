import os

command_file = os.getcwd()


def List_commands():
    with open(f"{command_file}/commands.txt") as file:
        read_data = file.read()
        print(read_data )
        return