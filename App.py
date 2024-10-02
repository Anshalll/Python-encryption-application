import sys
from cryptography.fernet import Fernet
import os
from functions.encryption_function import FilebasicEncrypt
from functions.decryptfile_function import Filebasicdecrypt
from functions.command_available import List_commands
from  functions.checkprogramfiles import Check_program_file

class Loadkey:
    def returnkey(self):
    
        try:
            with open("locals.env" , "r") as file:
                key = file.readlines()
                
                if not key:
                    sys.stderr.write("No key found,  please generate a key!")
                    sys.exit(1)
                else:
                    return key[0]
        except Exception :
           
            sys.stderr.write("No key found,  please generate a key!")
            sys.exit(1)
          
class BulkEncrypt(Loadkey):
    def bulk_encrypt(self, filepath): 
        try:
            if os.path.isdir(filepath):
               key = super().returnkey()
               fernet = Fernet(key)
               
               if not os.path.isdir(filepath):
                   sys.stdin.write('Provided path should be a directory')
                   sys.exit(1)

               for root , dir , files in os.walk(filepath): 
                   for file in files:
                    path = os.path.join(root, file)
               
                    if os.path.isfile(path):
                        FilebasicEncrypt(path , fernet)
                       
            else:
                sys.stdout.write("Provided path should be a folder")
                sys.exit(1)

        except Exception:
            sys.exit(1)

class Bulkdecrypt(Loadkey):
    def bulk_decrypt(self, filepath): 
        try:
            if os.path.isdir(filepath):
               key = super().returnkey()
               fernet = Fernet(key)

               if not os.path.isdir(filepath):
                   sys.stdin.write('Provided path should be a directory')
                   sys.exit(1)

               for root , dir, files in os.walk(filepath): 
                   for file in files:
                    full_path = os.path.join(root , file)

                    
                    if os.path.isfile(full_path):
                        Filebasicdecrypt(full_path , fernet)
                       
            else:
                sys.stdout.write("Provided path should be a folder")
                sys.exit(1)

        except Exception:
            sys.exit(1)

class EncryptFile(Loadkey):
    
    def encrypt(self , filename):
        key = super().returnkey()
        fernet = Fernet(key)
       
        if os.path.exists(filename):
            validate_File = filename.split(".")
            if "txt" in validate_File:
                FilebasicEncrypt(filename , fernet)
            else: 
                filename = f"{filename}.txt"
                FilebasicEncrypt(filename , fernet)
        else:
            sys.stderr.write("No such file found")

class DecryptFile(Loadkey):

    def decrypt(self , filename):
        key = super().returnkey()
        fernet = Fernet(key)

        if os.path.exists(filename):
            validate_File = filename.split(".")
            if "txt" in validate_File:
                Filebasicdecrypt(filename , fernet)
            else: 
                filename = f"{filename}.txt"
                Filebasicdecrypt(filename , fernet)
        else:
            sys.stderr.write("No such file found")


class GenerateKey:
    def generate_key(self , filepath):

        if not os.path.exists(filepath):

            key = Fernet.generate_key()

            with open(filepath, "wb") as file:
                file.write(key)
                sys.stdout.write("key generated!")
        else:
            with open(filepath, "r") as file:
                lines = file.readlines()

                if len(lines) > 0:
                    sys.stdout.write("Key already exists!")
                else:
                    key = Fernet.generate_key()

                    with open(filepath, "wb") as file:
                        file.write(key)
                        sys.stdout.write("key generated!")



class User_commands(GenerateKey , EncryptFile , DecryptFile , BulkEncrypt , Bulkdecrypt):
    def __init__(self, command , filepath  ):
 
        self.filepath = filepath
        self.command = command

        if self.command == "encrypt":
            super().encrypt(filepath)
        elif self.command == "decrypt":
            super().decrypt(filepath)
        elif self.command == "bulkencrypt":
            super().bulk_encrypt(filepath)
        elif self.command == "generatekey":
            super().generate_key(filepath)
        elif self.command == "bulkdecrypt":
            super().bulk_decrypt(filepath)
        else:
            sys.stderr.write(f"Unknown command {command}")


if __name__ == "__main__":
    try: 
        if len(sys.argv) < 2: 
            List_commands()
            sys.exit(1)

        command = sys.argv[1]
        filepath = sys.argv[2] if len(sys.argv) > 2 else None

     
        valid_commands = ["generatekey", "encrypt", "decrypt", "bulkencrypt", "bulkdecrypt"]
        
        if command not in valid_commands:
            print("unknown command")
            List_commands()
            sys.exit(1)


      
        if command in ["encrypt", "decrypt", "bulkencrypt", "bulkdecrypt"] and not filepath:
            print(f"Command '{command}' requires a filepath.")
            List_commands()
            sys.exit(1)
            
        if command == "generatekey":
       
            ucommands = User_commands(command, filepath='locals.env')
            sys.exit(0) 

        if Check_program_file(filepath): 
            print("Can't perform operations on program files")
            sys.exit(1)

 
        ucommands = User_commands( command, filepath)

    except Exception as e:
        print(e)
        List_commands()

