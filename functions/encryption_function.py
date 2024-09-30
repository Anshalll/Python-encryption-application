import sys

def FilebasicEncrypt(filename , fernet):
    with open(filename , "rb") as file: 
        filedata = file.read()
        
        encrypted_data = fernet.encrypt(filedata)

    with open(filename , 'wb') as file:
                file.write(encrypted_data)
            
    sys.stdout.write(f"Encrypted {filename} \n")