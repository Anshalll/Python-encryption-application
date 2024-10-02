import os

files = [
    'functions' , 'locals.env' , 'App.py' , 'README.md' , 'commands.txt' , 
]

def Check_program_file(path):
    for file in files:

        program_files = os.path.join(os.getcwd(), file)


        if os.path.isabs(path):
            if path.startswith(program_files):
         
                return True

        else:
            abs_path = os.path.abspath(path)
            if abs_path.startswith(program_files):
                return True


