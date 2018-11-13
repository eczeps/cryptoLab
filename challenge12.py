#4
import base64
from challenge10 import AESencrypt
from challenge11 import random16Bytes, next16Multiple, detectECBorCBC
from challenge09 import PKCS7pad
from challenge15 import stripPKCS7


KEY = random16Bytes()

def main():
    blockSize = findBlockSize(KEY)
    ciphertext = ECBOracle(b"12345678901234561234567890123456")
    if detectECBorCBC(ciphertext) == "ECB":
        return breakECBOracle(blockSize)
    else:
        return None

def ECBOracle(yourString):
    #yourString should be a BYTEstring
    unknownString = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    decodedString = base64.b64decode(unknownString)
    totalString = yourString + decodedString
    targetLen = next16Multiple(len(totalString))
    paddedPlaintext = PKCS7pad(totalString, targetLen)
    ciphertext = AESencrypt(paddedPlaintext, KEY)
    return ciphertext
    
def findBlockSize(key):
    #idk
    #keep adding bytes until the length of the ciphertext jumps and see how much it jumps by
    return 16
    
    
    
def getByteOfPlaintext(blockSize, whichByte, bytesSoFar, whichBlock):
    #whichBlock starts at 0!
    #whichByte is the index of the byte we're looking for
    yourString = b'A'*(whichByte)
    ciphertext = ECBOracle(yourString)
    possibilityDict = dictOfOutputs(yourString, bytesSoFar)
    for k, v in possibilityDict.items():
        if ciphertext[whichBlock*blockSize:(whichBlock + 1)*blockSize] == v[whichBlock*blockSize:(whichBlock + 1)*blockSize]: 
            return k
    return None
    
    
    
def dictOfOutputs(repeatingString, bytesSoFar):
    #{b"A": ECBOracle(b"AAAAAA"), b"B": ECBOracle(b"AAAAAAB")}
    result = {}
    lastBytes = [bytes([x]) for x in range(256)]
    for byte in lastBytes:
        result[byte] = ECBOracle(repeatingString + bytesSoFar + byte)
    return result
    
    
def breakECBOracle(blockSize):
    result = b""
    iterList = range(blockSize)[::-1] #reversed
    whichBlock = 0
    try:
        while True:
            #this is a little bit yikes but it's just going to keep looping until
            #we get to the end of the string we're figuring out
            #hard to make a condition because we don't know how long that string is
            #the condition here is essentially loop while we don't have an exception
            for i in iterList:
                #i is the index of the byte we're looking for within the given block
                thisByte = getByteOfPlaintext(blockSize, i, result, whichBlock)
                result += thisByte
            whichBlock += 1
    except TypeError:
        #we just reached the end of the string we're finding
        pass
    return stripPKCS7(result, blockSize)