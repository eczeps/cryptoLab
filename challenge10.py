#1.5
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from challenge06 import bytesXOR, parseFile, base64StringToBytes
from challenge09 import PKCS7pad

def main(filename):
    ciphertext = parseFile(filename)
    ciphertext = base64StringToBytes(ciphertext)
    decrypted = CBCdecrypt(ciphertext, b"YELLOW SUBMARINE", b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    encrypted = CBCencrypt(decrypted, b"YELLOW SUBMARINE", b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    return encrypted == ciphertext
    
    


def CBCdecrypt(ciphertext, key, IV):
    listOfBlocks = getListOfBlocks(ciphertext)
    previousBlock = IV
    result = b""
    for i in range(len(listOfBlocks)):
        thisBlock = listOfBlocks[i]
        decrypted = AESdecrypt(thisBlock, key)
        xord = bytesXOR(previousBlock, decrypted)
        result += xord
        previousBlock = thisBlock
    return result


def CBCencrypt(plaintext, key, IV):
    listOfBlocks = getListOfBlocks(plaintext)
    previousBlock = IV
    result = b""
    for i in range(len(listOfBlocks)):
        thisBlock = listOfBlocks[i]
        xord = bytesXOR(previousBlock, thisBlock)
        encrypted = AESencrypt(xord, key)
        previousBlock = encrypted
        result += encrypted
    return result
    

def getListOfBlocks(plaintext):
    #assuming we want 128 bit blocks -- 16 byte blocks
    result = []
    for i in range(len(plaintext)):
        if i%16 == 0:
            result.append(bytes([plaintext[i]]))
        else:
            result[-1] += bytes([plaintext[i]])
    if len(result[-1]) != 16:
        print('hello')
        result[-1] = PKCS7pad(result[-1], 16)
    return result
    
    

def AESdecrypt(ciphertext, key):
    backend = default_backend()
    algorithm = algorithms.AES(key)
    mode = modes.ECB()
    cipher = Cipher(algorithm, mode, backend=backend)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()
    
    
    
def AESencrypt(plaintext, key):
    backend = default_backend()
    algorithm = algorithms.AES(key)
    mode = modes.ECB()
    cipher = Cipher(algorithm, mode, backend=backend)
    encryptor = cipher.encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()