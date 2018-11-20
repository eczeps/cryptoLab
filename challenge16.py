#1

from challenge11 import random16Bytes, next16Multiple
from challenge10 import CBCencrypt, CBCdecrypt
from challenge09 import PKCS7pad
from challenge15 import stripPKCS7

KEY = random16Bytes()
IV = random16Bytes()

def main():
    print("breaking the cipher and checking for ;admin=true;")
    return breakCipher()


def concatAndEncrypt(plaintext):
    prepend = b"comment1=cooking%20MCs;userdata="
    append = b";comment2=%20like%20a%20pound%20of%20bacon"
    plaintext = cleanPlaintext(plaintext)
    longPlaintext = prepend + plaintext + append
    nextMult = next16Multiple(len(longPlaintext))
    fullPlaintext = PKCS7pad(longPlaintext, nextMult)
    ciphertext = CBCencrypt(fullPlaintext, KEY, IV)
    return ciphertext
    
def cleanPlaintext(plaintext):
    result = b""
    for char in plaintext:
        if bytes([char]) != b';' and bytes([char]) != b'=':
            result += bytes([char])
        else:
            result += b'%'
    return result
    
    
def decryptAndCheck(ciphertext):
    decryption = CBCdecrypt(ciphertext, KEY, IV)
    stripped = stripPKCS7(decryption, 16)
    print(stripped)
    if b";admin=true;" in stripped:
        return True
    return False
    
    
def breakCipher():
    exploit = b":admin<true"
    #to fix it, we need to flip the least significant bit in the : and the <
    ciphertext = concatAndEncrypt(exploit)
    #assumes a block size of 16
    #our exploit string begins at the beginning of the third block
    #we need to flip the least significant bits of indices 0 and 6 in the second block
    #aka indices 16 and 22
    #this all relies on the prepend string being static and knowing its length
    newCiphertext = b""
    for index in range(len(ciphertext)):
        if index != 16 and index !=22:
            newCiphertext += bytes([ciphertext[index]])
        else:
            newCiphertext += bytes([ciphertext[index] ^ 0x01])
    return decryptAndCheck(newCiphertext)
    