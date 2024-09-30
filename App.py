import sys
from cryptography.fernet import Fernet
import os
from functions.encryption_function import FilebasicEncrypt
from functions.decryptfile_function import Filebasicdecrypt

class Loadkey:
    def returnkey(self):
    
        try:
            with open("generated_key.txt" , "r") as file:
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
               items = os.listdir(filepath)

               for file in items: 
                   full_path = os.path.join(filepath, file)
                   if os.path.isfile(full_path):
                       FilebasicEncrypt(full_path , fernet)
                       
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
               items = os.listdir(filepath)

               for file in items: 
                   full_path = os.path.join(filepath, file)
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
    def generate_key(self):

        if not os.path.exists("generated_key.txt"):

            key = Fernet.generate_key()

            with open("generated_key.txt", "wb") as file:
                file.write(key)
                sys.stdout.write("key generated!")
        else:
            with open("generated_key.txt", "r") as file:
                lines = file.readlines()

                if len(lines) > 0:
                    sys.stdout.write("Key already exists!")
                else:
                    key = Fernet.generate_key()

                    with open("generated_key.txt", "wb") as file:
                        file.write(key)
                        sys.stdout.write("key generated!")



class User_commands(GenerateKey , EncryptFile , DecryptFile , BulkEncrypt , Bulkdecrypt):
    def __init__(self, scriptname, command , filepath  ):
        self.scriptname = scriptname
        self.filepath = filepath
        self.command = command

        if self.command == "encrypt":
            super().encrypt(filepath)
        elif self.command == "decrypt":
            super().decrypt(filepath)
        elif self.command == "bulkencrypt":
            super().bulk_encrypt(filepath)
        elif self.command == "generatekey":
            super().generate_key()
        elif self.command == "bulkdecrypt":
            super().bulk_decrypt(filepath)
        else:
            sys.stderr.write(f"Unknown command {command}")


if __name__ == "__main__":
    
    if  sys.argv[1] == "generatekey" and len(sys.argv) != 2:
        sys.stderr.write(
            "Unknown command \n commands available - \n \t generatekey \t eg= python <script name> generatekey"
        )
    
    elif sys.argv[1] == "encrypt" and len(sys.argv)  != 3: 
        sys.stderr.write(
            "Unknown command \n commands available - \n \t encrypt \t eg= python <script name> encrypt <file to encrypt>"
        )
    elif sys.argv[1] == "decrypt" and len(sys.argv) != 3 : 
        sys.stderr.write(
            "Unknown command \n commands available - \n \t decrypt \t eg= python <script name> decrypt <file to encrypt>"
        )
    elif sys.argv[1] == "bulkencryt" and len(sys.argv) != 3:
        sys.stderr.write(
            "Unknown command \n commands available - \n \t decrypt \t eg= python <script name> bulkencrypt <Folder_path>"
        )
    elif sys.argv[1] == "bulkdecrypt" and len(sys.argv) != 3:
        sys.stderr.write(
            "Unknown command \n commands available - \n \t decrypt \t eg= python <script name> bulkdecrypt <Folder_path>"
        )
    else:
        scriptname = sys.argv[0]
        command = sys.argv[1]
        filepath = None
        
        if command == "encrypt" or command == "decrypt":
            filepath = sys.argv[2]

            ucommnds = User_commands(scriptname, command , filepath)
        if command == "bulkencrypt" or command == "bulkdecrypt":
            filepath = sys.argv[2]
            ucommnds = User_commands(scriptname, command , filepath)
        else:
             ucommnds = User_commands(scriptname, command , filepath=None)