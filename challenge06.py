#6; includes time making 3 and 4 compatible
from challenge03 import decrypt
from challenge05 import generateKey
import base64


def main(filename):
    #ciphertext should be a bytes string
    ciphertext = parseFile(filename)
    ciphertext = base64StringToBytes(ciphertext)
    #keySize = findKeySize(ciphertext)
    #print(keySize)
    keySize = 29
    listOfBlocks = getListOfBlocks(ciphertext, keySize)
    transposedBlocks = getTransposedBlocks(listOfBlocks)
    key = getKey(transposedBlocks, keySize)
    print(key)
    #key = b'Terminator X: Bring the noise'
    #print(key)
    longKey = generateKey(ciphertext, key.decode())
    plaintext = bytesXOR(longKey, ciphertext)
    #write an xor function that takes in bytes
    return plaintext
  
'''this works'''  
def bytesXOR(bytes1, bytes2):
    xored = bytes([a^b for (a, b) in zip(bytes1, bytes2)])
    return xored
    
def base64ToHexBytes(result):
    return base64.decodebytes(result)
    
def base64StringToBytes(ciphertext):
    normalString = base64.b64decode(ciphertext)
    return normalString
    
def base64BytesToHexBytes(ciphertext):
    base64String = ciphertext.decode()
    normalString = base64.b64decode(base64String)
    hexString = base64.b16encode(normalString)
    return hexString
    
    
def bytesStringToHexString(bytesString):
    return base64.b16encode(bytesString)
    
    
'''FIRST ORDER OF BUSINESS: MAKE THIS WORK ON ALL HEX STRINGS




V IMPORTANT



DO FIRST

'''
def asciiHexToBytes(asciiHexStr):
    return base64.b16decode(asciiHexStr)
    
'''this works'''
def parseFile(filename):
    result = ""
    with open(filename, 'r') as textfile:
        result = textfile.read()
    result = result.encode()
    #result = base64ToHexBytes(result)
    return result


'''pretty sure this works'''   
def hammingDistance(bytes1, bytes2):
    #  assumes bytes1 >= bytes2
    ham = 0
    for i in range(len(bytes2)):
        bin1 = bin(bytes1[i])
        bin2 = bin(bytes2[i])
        #bin1 and bin2 include an 0b at the beginning -- get rid of it:
        bin1 = bin1[2:]
        bin2 = bin2[2:]
        #bin1 and bin2 will drop any leading 0s, which we need to fix
        bin1 = (8 - len(bin1))*'0' + bin1
        bin2 = (8 - len(bin2))*'0' + bin2
        #now loop through each bit in bins
        for j in range(len(bin2)):
            if bin1[j] != bin2[j]:
                ham += 1
    if len(bytes1) > len(bytes2):
        #8 bits per byte, char is 2 bytes, so we multiply by 4
        ham += (len(bytes1) - len(bytes2))
    return ham
    
'''
this works, but takes in strings and I wanted it to take in bytes
def hammingDistance(string1, string2):
    #  assumes string1 >= string2
    ham = 0
    #bytes1 = binascii.a2b_qp(string1)
    #bytes2 = binascii.a2b_qp(string2)
    bytes1 = string1.encode()
    bytes2 = string2.encode()
    for i in range(len(bytes2)):
        bin1 = bin(bytes1[i])
        bin2 = bin(bytes2[i])
        #bin1 and bin2 include an 0b at the beginning -- get rid of it:
        bin1 = bin1[2:]
        bin2 = bin2[2:]
        #bin1 and bin2 will drop any leading 0s, which we need to fix
        bin1 = (8 - len(bin1))*'0' + bin1
        bin2 = (8 - len(bin2))*'0' + bin2
        #now loop through each bit in bins
        for j in range(len(bin2)):
            if bin1[j] != bin2[j]:
                ham += 1
    if len(string1) > len(string2):
        #8 bits per byte, char is 2 bytes, so we multiply by 4
        ham += (len(string1) - len(string2))*4
    return ham
    '''
def findKeySize(bytesString):
    #think real hard if this should take a string or bytes
    bestKEYSIZE = 0
    shortestDistance = len(bytesString)
    for KEYSIZE in range(2, min(40, len(bytesString) -1)):
        first = bytesString[:KEYSIZE]
        try:
            second = bytesString[KEYSIZE:2*KEYSIZE]
        except IndexError:
            print('index error')
            second = bytesString[KEYSIZE:]
        distance = hammingDistance(first, second)
        normalizedDistance = distance/KEYSIZE
        if normalizedDistance < shortestDistance:
            print(normalizedDistance)
            shortestDistance = normalizedDistance
            bestKEYSIZE = KEYSIZE
    return bestKEYSIZE
    
def getListOfBlocks(bytesString, keySize):
    #ASSUMES KEYSIZE <= LEN(BYTESSTRING)
    result = []
    numBlocks = int(len(bytesString)/keySize)
    for block in range(numBlocks):
        result.append(bytesString[block*keySize:(block+1)*keySize])
    #the above code cuts off chars that don't fit evenly, so we add htem ourselves:
    if (block + 1)*keySize < len(bytesString):
        result.append(bytesString[(block+1)*keySize:])
    return result
    
def getTransposedBlocks(listOfBlocks):
    #TAKES IN LIST OF BYTESTRINGS. ALL MUST BE EQUAL LENGTH EXCEPT THE LAST ONE
    result = []
    numTransposedBlocks = len(listOfBlocks[0])
    for transposedBlock in range(numTransposedBlocks):
        #listOfBlocks is in a list because bytes takes a list of ints
        result.insert(transposedBlock, bytes([listOfBlocks[0][transposedBlock]]))
        for i in range(1, len(listOfBlocks)):
            try:
                result[transposedBlock] += bytes([listOfBlocks[i][transposedBlock]])
            except IndexError:
                #this just happens on the last item in listOfBlocks. nbd
                pass
    return result

def getKey(listOfTransposedBlocks, keySize):
    key = ""
    for i in range(keySize):
        thisblock = listOfTransposedBlocks[i]
        hexstr = bytesStringToHexString(thisblock)
        decryption = decrypt(hexstr)
        #key should be a bytes string that looks like b'abc'
        hexStrChar = str(decryption[1])[2:4]
        #key += chr((int(str(decryption[1])[2:4])))
        key += hexStrChar[0].upper()
        key += hexStrChar[1].upper()
    print(key)
    return asciiHexToBytes(key)

