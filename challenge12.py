#3
import base64
from challenge10 import AESencrypt
from challenge11 import random16Bytes, next16Multiple, detectECBorCBC
from challenge09 import PKCS7pad


KEY = random16Bytes()

def main():
    blockSize = findBlockSize(KEY)
    if detectECBorCBC() == "ECB":
        yourString = b"A"*(blockSize - 1)
    ciphertext = ECBOracle(yourString)
    return ciphertext

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
    return 16
    
    '''
def getByteOfPlaintext(whichByte, bytesSoFar):
    #assert len(bytesSoFar) + whichByte = blockSize
    yourString = b'A'*(whichByte)
    ciphertext = ECBOracle(yourString)
    possibilityDict = dictOfOutputs(yourString, whichByte)
    #all this indexing nonsense is so we only compare the repeating bytes and one after
    if whichByte == 1:
        #when it's -1 you can't do +1 because it'll wrap around
        condition = ciphertext
    else:
        condition = ciphertext[:-whichByte + 1]
    for k, v in possibilityDict.items():
        #not sure this indexing is right
        if condition == v:
            return k
    return None
    
    
    
def dictOfOutputs(repeatingString, whichByte):
    #{b"A": ECBOracle(b"AAAAAA"), b"B": ECBOracle(b"AAAAAAB")}
    result = {}
    lastBytes = [bytes([x]) for x in range(256)]
    if whichByte == 1:
        index = ""
    else:
         index = -whichByte + 1
    for byte in lastBytes:
        result[byte] = ECBOracle(repeatingString + byte)[:index]
    return result
    
    
def breakECBOracle(blockSize):
    result = b""
    for i in range(1, blockSize):
        thisByte = getByteOfPlaintext(blockSize, i)
        result += thisByte
    return result
    '''
    
def getByteOfPlaintext(blockSize, whichByte, bytesSoFar, whichBlock):
    #whichBlock starts at 0!
    #whichByte is the index of the byte we're looking for
    yourString = b'A'*(whichByte)
    ciphertext = ECBOracle(yourString)
    possibilityDict = dictOfOutputs(yourString, bytesSoFar)
    for k, v in possibilityDict.items():
        if ciphertext[whichBlock*16:(whichBlock + 1)*16] == v[whichBlock*16:(whichBlock + 1)*16]: 
            return k
    return None
    
    
    
def dictOfOutputs(repeatingString, bytesSoFar):
    #{b"A": ECBOracle(b"AAAAAA"), b"B": ECBOracle(b"AAAAAAB")}
    result = {}
    lastBytes = [bytes([x]) for x in range(256)]
    print(repeatingString + lastBytes[2] + bytesSoFar)
    for byte in lastBytes:
        result[byte] = ECBOracle(repeatingString + bytesSoFar + byte)
    return result
    
    
def breakECBOracle(blockSize):
    result = b""
    iterList = range(blockSize)[::-1] #reversed
    whichBlock = 0
    try:
        while True:
            for i in iterList:
                #i is the index of the byte we're looking for
                print(i)
                #whichBlock has to start at 0!
                thisByte = getByteOfPlaintext(blockSize, i, result, whichBlock)
                result += thisByte
                print(result)
            whichBlock += 1
    except Exception:
        #we just reached the end of the string we're finding
        pass
    return result