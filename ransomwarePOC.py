from cryptography.fernet import Fernet, InvalidToken
import base64
import os
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

def generateKey():
    key = Fernet.generate_key()
    #Instead of writing to a file, would send to our database if we wanted to go that far
    file = open('key.key', 'wb')
    file.write(key)
    file.close
    return key

def encryptFile(filePath, key):
    with open(filePath, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    outputFile = filePath + '.encrypted'

    with open(outputFile, 'wb') as f:
        f.write(encrypted)

    os.remove(filePath)
    return outputFile

def decryptFile(filePath, key):
    output_file = filePath.replace('.encrypted', '')

    with open(filePath, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(data)

        with open(output_file, 'wb') as f:
            f.write(decrypted)

        os.remove(filePath)
        return True
    except InvalidToken as e:
        print("Invalid Key - Unsuccessfully decrypted")
        return False


key = generateKey()
encryptedFile = encryptFile("test.txt", key)
needKey = True
while(needKey):
    newKey = input("Enter key: ")
    needKey = not decryptFile(encryptedFile, newKey)
print("Successfully decrypted file")

