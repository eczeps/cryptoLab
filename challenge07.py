#1 hr


import binascii
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def main(filename, key):
    ciphertext = parseFile(filename)
    plaintext = AESdecrypt(ciphertext, key)
    return plaintext
    
def parseFile(filename):
    result = ""
    with open(filename, 'r') as textfile:
        for line in textfile:
            result += line
    return binascii.a2b_qp(result)
    

def AESdecrypt(ciphertext, key):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB, backend=backend)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()