#2 hr


import binascii
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def main(filename, key):
    ciphertext = parseFile(filename)
    print(ciphertext[:40])
    plaintext = AESdecrypt(ciphertext, key)
    return plaintext
    
def parseFile(filename):
    result = ""
    with open(filename, 'r') as textfile:
        for line in textfile:
            result += line 
    print(result[:40])
    return result.encode()
    

def AESdecrypt(ciphertext, key):
    key2 = os.urandom(32)
    print(key2)
    backend = default_backend()
    algorithm = algorithms.AES(key)
    mode = modes.ECB()
    cipher = Cipher(algorithm, mode, backend=backend)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()
    