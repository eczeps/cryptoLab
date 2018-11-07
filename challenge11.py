#3 hrs
from random import *
from challenge10 import *
from challenge09 import PKCS7pad
from challenge08 import numRepeatedBlocks
from challenge06 import parseFile, base64StringToBytes


'''somehow it works on 11test1.txt but not 11test2.txt. the repeated block
counting function is messed up but it's super unclear why??? '''

def main(filename):
    plaintext = parseFile(filename)
    ciphertext = encryptionOracle(plaintext)
    print(ciphertext)
    return detectECBorCBC(ciphertext)

def detectECBorCBC(ciphertext):
    #score gets incremented for ECB, decremented for CBC
    score = 0
    #repeatedBlocks are only helpful if len >= 32
    repeatedBlocks= numRepeatedBlocks(ciphertext)
    print(repeatedBlocks)
    score += repeatedBlocks
    if score > 0:
        return "ECB"
    else:
        return "CBC"

    
def encryptionOracle(plaintext):
    key = random16Bytes()
    padLens = randrange(5, 11)
    plaintext = padPlaintext(plaintext, padLens, padLens)
    ECBorCBC = randrange(0, 2)
    if ECBorCBC == 1:
        print("using ECB")
        length = next16Multiple(len(plaintext))
        plaintext = PKCS7pad(plaintext, length)
        ciphertext = AESencrypt(plaintext, key)
    else:
        print("using CBC")
        IV = random16Bytes()
        ciphertext = CBCencrypt(plaintext, key, IV)
    return ciphertext
    

def random16Bytes():
    result = b''
    for i in range(16):
        thisInt = randrange(0, 256)
        result += bytes([thisInt])
    return result
    
    
def padPlaintext(plaintext, frontPadLen, backPadLen):
    #plaintext is bytes, padlens are ints
    return bytes([frontPadLen])*frontPadLen + plaintext + bytes([backPadLen])*backPadLen
    
def next16Multiple(anchor):
    #returns the next multiple of 16 after anchor
    result = 0
    while (anchor + result)%16 != 0:
        result += 1
    return result + anchor