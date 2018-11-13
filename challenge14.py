#2

#random count of bytes added to plaintext should be larger than the blocksize and
#also should be constant! as in the bytes are random but the count is constant

'''
my strategy is to do the same thing as in 12 for all the blocks that are just 
the unknown string, adn for the block that's partly random bytes, just only
iterate through the bytes in that block that aren't random. is that the right
strategy
'''

from random import *
import math
import base64
from challenge10 import AESencrypt
from challenge09 import PKCS7pad
from challenge15 import stripPKCS7
from challenge11 import random16Bytes, next16Multiple, detectECBorCBC


#RANDOMCOUNT = randrange(17, 256)
RANDOMCOUNT = 32
KEY = random16Bytes()

def ECBOracle14(yourString):
    #yourString should be a BYTEstring
    unknownString = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    decodedString = base64.b64decode(unknownString)
    totalString = getRandomBytes() + yourString + decodedString
    targetLen = next16Multiple(len(totalString))
    paddedPlaintext = PKCS7pad(totalString, targetLen)
    ciphertext = AESencrypt(paddedPlaintext, KEY)
    return ciphertext
    
    
def getRandomBytes():
    result = b""
    for byte in range(RANDOMCOUNT):
        thisInt = randrange(0, 256)
        result += bytes([thisInt])
    return result
    

def getByteOfPlaintext14(blockSize, whichByte, bytesSoFar, whichBlock):
    #whichBlock starts at 0!
    #whichByte is the index of the byte we're looking for
    yourString = b'A'*(whichByte)
    ciphertext = ECBOracle14(yourString)
    possibilityDict = dictOfOutputs14(yourString, bytesSoFar)
    for k, v in possibilityDict.items():
        if ciphertext[whichBlock*blockSize + RANDOMCOUNT:(whichBlock + 1)*blockSize + RANDOMCOUNT] == v[whichBlock*blockSize + RANDOMCOUNT:(whichBlock + 1)*blockSize + RANDOMCOUNT]: 
            return k
    return None
    
    
    
def dictOfOutputs14(repeatingString, bytesSoFar):
    #{b"A": ECBOracle(b"AAAAAA"), b"B": ECBOracle(b"AAAAAAB")}
    result = {}
    lastBytes = [bytes([x]) for x in range(256)]
    for byte in lastBytes:
        result[byte] = ECBOracle14(repeatingString + bytesSoFar + byte)
    return result
    
    
def breakECBOracle14(blockSize):
    result = b""
    iterList = range(blockSize)[::-1] #reversed
    #whichBlock should start at the first block that's partly random bytes & partly
    #the attacker-controlled string
    whichBlock = math.floor(RANDOMCOUNT/blockSize) - 1 
    if RANDOMCOUNT%blockSize != 0:
        print("hello")
        for byte in range(RANDOMCOUNT%blockSize + 1, blockSize)[::-1]:
            #the first time, because of the random bytes the thing could start in the middle
            #of a block
            thisByte = getByteOfPlaintext14(blockSize, byte, result, whichBlock)
            result += thisByte
        whichBlock += 1
    try:
        while True:
            print(whichBlock)
            print(result)
            #this is a little bit yikes but it's just going to keep looping until
            #we get to the end of the string we're figuring out
            #hard to make a condition because we don't know how long that string is
            #the condition here is essentially loop while we don't have an exception
            for i in iterList:
                #i is the index of the byte we're looking for within the given block
                thisByte = getByteOfPlaintext14(blockSize, i, result, whichBlock)
                result += thisByte
            whichBlock += 1
    except TypeError:
        #we just reached the end of the string we're finding
        pass
    return stripPKCS7(result, blockSize)