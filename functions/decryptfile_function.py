import sys

def Filebasicdecrypt(filename , fernet):
    with open(filename , "rb") as file: 
        filedata = file.read()
        
        decrypted_data = fernet.decrypt(filedata)

    with open(filename , 'wb') as file:
                file.write(decrypted_data)
            
    sys.stdout.write(f"decrypted {filename} \n")