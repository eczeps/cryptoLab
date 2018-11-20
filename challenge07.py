#2 hrs


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def main(filename="7.txt", key=b"YELLOW SUBMARINE"):
    print("decrypting file " + filename + " under the key " + key.decode())
    ciphertext = parseFile(filename)
    plaintext = AESdecrypt(ciphertext, key)
    return plaintext
    
def base64ToBytes(result):
    return base64.decodebytes(result)
    
def parseFile(filename):
    result = ""
    with open(filename, 'r') as textfile:
        result = textfile.read()
    result = result.encode()
    result = base64ToBytes(result)
    return result
    

def AESdecrypt(ciphertext, key):
    backend = default_backend()
    algorithm = algorithms.AES(key)
    mode = modes.ECB()
    cipher = Cipher(algorithm, mode, backend=backend)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()
    