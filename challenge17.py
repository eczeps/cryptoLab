#6.5

'''these were super helpful resources I used to help understand padding oracle 
attacks. some of them include code, I just didn't watch/read those parts'''
#https://blog.cloudflare.com/padding-oracles-and-the-decline-of-cbc-mode-ciphersuites/
#https://en.wikipedia.org/wiki/Padding_oracle_attack
#https://www.youtube.com/watch?v=pEdGUSGi1iM
#https://blog.skullsecurity.org/2013/padding-oracle-attacks-in-depth


'''NOTE:
this exploit is not finished! When you run it you should get a type error that
zip argument #1 must support iteration. This just means it didn't find any 
correct padding for one of the bytes, and it fails on the next iteration because
the previous byte is None.  I think there's an off by one error here -- I read
the articles above and really feel like I understand the theory/concepts, just 
couldn't get the code to actually work'''

from challenge11 import random16Bytes, next16Multiple
from random import *
from challenge10 import CBCencrypt, CBCdecrypt, getListOfBlocks
from challenge09 import PKCS7pad
from challenge06 import bytesXOR




'''REMEMBER TO MAKE IT RANDOM AGAIN AT THE END'''

#KEY = random16Bytes()
KEY = b'\xba3"\x84mS\xc4\xa5\x8c\x9e\xf9 \xffDrQ'
#IV = random16Bytes()
IV = b'^\xc5Q\xe5D\xb0w\x98\xdf\x16.\x0f.\\H\xb0'





def main():
    try:
        paddingOracleAttack()
    except TypeError:
        print()
        print()
        print("we got a type error! it's okay. just means we didn't find any\
        correct padding for our previous block. this challenge doesn't completely\
        work")



def encryptAString():
    possibilities = [b"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
b"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
b"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
b"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
b"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
b"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
b"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
b"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
b"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
b"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"]
    #index = randrange(0, len(possibilities))
    #MAKE IT RANDOM HERE TOO
    index = 2
    mult = next16Multiple(len(possibilities[index]))
    padded = PKCS7pad(possibilities[index], mult)
    ciphertext = CBCencrypt(padded, KEY, IV)
    return ciphertext
    
    
def decryptAndCheck(ciphertext):
    decrypted = CBCdecrypt(ciphertext, KEY, IV)
    return checkPKCS7pad(decrypted, 16)
    

def checkPKCS7pad(byteString, blockSize):
    lastByte = byteString[-1]
    #assumes block size of 16 AND that there is at least some padding
    if lastByte in bytes(range(blockSize)):
        for i in range(1, lastByte + 1):
            if byteString[-i] != lastByte:
                #invalid PKCS7 padding
                return False
        return True
    return False
    
    
def paddingOracleAttack(blockSize=16):
    #all the naming conventions here are from the skullsecurity blog post
    ciphertext = encryptAString()
    cprime = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    blocks = getListOfBlocks(ciphertext)
    potentialBytes = bytes(range(256))
    #plaintexts just needs to be a list of lists of length blockSize
    plaintexts = [[None]*blockSize for x in range(len(blocks))]
    for index in range(len(blocks))[::-1]:
        #currentBlock is the one we're currently trying to break
        #it corresponds to CsubN in the articles I was reading
        currentBlock = blocks[index]
        for k in range(blockSize)[::-1]:
            print("k at beginning", k)
            
            '''setting up testcprime'''
            
            encryptedpad = b"\x10"
            if k != len(cprime) - 1 and k != 0:
                temp = bytesXOR(plaintexts[index][k + 1], bytes([blocks[index -1][k + 1]]))
                encryptedpad = bytesXOR(bytes([blockSize - k]), temp)
                print("got encryptedpad")
            for byte in potentialBytes:
                testcprime = b""
                #set cprime[k] = potentialByte:
                for j in range(len(cprime)):
                    if k == j:
                        testcprime += bytes([byte])
                    elif j > k:
                        testcprime += encryptedpad
                    else:
                        testcprime += bytes([cprime[j]])
                        
                        
                        
                print("testcprime", testcprime)        
                exploitString = testcprime + currentBlock
                pprime = decryptAndCheck(exploitString)
                if pprime == True:
                    print("found correct padding!")
                    temp = bytesXOR(bytes([blocks[index - 1][k]]), bytes([testcprime[k]]))
                    print("K", k)
                    print("index", index)
                    print("plaintexts", plaintexts)
                    plaintexts[index][k] = bytesXOR(bytes([blockSize - k]), temp)
                    print("xor constant", blockSize - k)
                    print("plaintexts so far", plaintexts)
                    break
    return plaintexts
        
        
"""
def paddingOracleAttack(blockSize=16):
    ciphertext = encryptAString()
    listOfBlocks = getListOfBlocks(ciphertext)
    totalDecrypted = [x for x in range(blockSize)]
    for i in range(len(listOfBlocks))[::-1]:
        if i != 0:
            totalDecrypted[i] = breakOneBlock(listOfBlocks[i-1])
        else:
            print("couldn't get last block, unsure what to do, pls send help")
    return totalDecrypted
    

def breakOneBlock(c1, blockSize=16):
    #c2 is a block of ciphertext PRECEEDING the block we're breaking
    #p2 just has to be a list of length blockSize
    p2 = [bytes([x]) for x in range(blockSize)]
    #blockBytes should be like [15, 14, 13...0]
    blockBytes = range(blockSize)[::-1]
    potentialBytes = bytes(range(256))
    for byte in blockBytes:
        padding = (blockSize - byte)*bytes([blockSize - byte])
        evilC = b""
        if byte < blockSize - 1:
            print('hello')
            #if we're not on the 15th byte, set the end to be padding
            for i in range(len(c1)):
                if i > byte:
                    evilC += bytes([blockSize - byte])
                else:
                    evilC += bytes([c1[i]])
        else:
            evilC = c1
        print("evilC", evilC)
        #done setting padding, time to try potential bytes
        for potentialByte in potentialBytes:
            #put potentialByte in as padding. this is a terrible way to do it
            testC = b""
            for j in range(1, len(evilC)):
                if j == byte:
                    testC += bytes([potentialByte])
                else:
                    testC += bytes([evilC[j]])
            validPadding = decryptAndCheck(testC)
            if validPadding:
                print("byte", byte)
                print("c1", c1)
                print("testC",testC)
                xord = bytesXOR(testC, padding)
                print("xord", xord)
                print()
                p2[byte] = bytes([xord[0]])
                #break out of inner for loop
                break
    return b''.join(p2)
            
            
    """