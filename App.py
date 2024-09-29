import sys
from cryptography.fernet import Fernet
import os
from functions.encryption_function import FilebasicEncrypt
from functions.decryptfile_function import Filebasicdecrypt

class Loadkey:
    def returnkey(self):
    
        try:
            with open("generated_key.txt" , "r") as file:
                key = file.readlines().strip()
                if not key:
                    sys.stderr.write("No key found,  please generate a key!")
                    sys.exit(1)
                else:
                    return key[0]
        except Exception:
            sys.stderr.write("No key found,  please generate a key!")
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






class User_commands(GenerateKey , EncryptFile , DecryptFile):
    def __init__(self, scriptname, command , filename):
        self.scriptname = scriptname
        self.filename = filename
        self.command = command

        if self.command == "encrypt":
            super().encrypt(filename)
        elif self.command == "decrypt":
            super().decrypt(filename)

        elif self.command == "generatekey":
            super().generate_key()
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
    else:
        scriptname = sys.argv[0]
        command = sys.argv[1]
        filename = None
        
        if command == "encrypt" or command == "decrypt":
            filename = sys.argv[2]

        ucommnds = User_commands(scriptname, command , filename)
