#6.5; includes time making 3 and 4 compatible
from challenge03 import decryptSingleCharKey
import base64


def main(filename):
    ciphertext = parseFile(filename)
    #ciphertext should be a bytes string
    ciphertext = base64StringToBytes(ciphertext)
    return decryptRepeatingKey(ciphertext)
    
    
def decryptRepeatingKey(ciphertext):
    #ciphertext should be bytes string
    keySize = findKeySize(ciphertext)
    print(keySize)
    listOfBlocks = getListOfBlocks(ciphertext, keySize)
    transposedBlocks = getTransposedBlocks(listOfBlocks)
    key = getKey(transposedBlocks, keySize)
    longKey = betterGenerateKey(ciphertext, key)
    plaintext = bytesXOR(longKey, ciphertext)
    return plaintext
    
#there's a bad version in challenge05
def betterGenerateKey(ciphertext, bytesKey):
    length = len(ciphertext)
    #this is the key repeated all the times its repeated fully. i.e. ICE not ICEI
    shortkey = bytesKey*(int((length/len(bytesKey))))
    mod = length%len(bytesKey)
    #adds the part that didn't divide evenly
    fullkey = shortkey + bytesKey[:mod]
    return fullkey
  

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
    

def asciiHexToBytes(asciiHexStr):
    #only works when letters in string are uppercase!!!
    return base64.b16decode(asciiHexStr)
    

def parseFile(filename):
    result = ""
    with open(filename, 'r') as textfile:
        result = textfile.read()
    result = result.encode()
    return result


  
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
        #feel like this never happens/this hasn't been tested
        ham += (len(bytes1) - len(bytes2))*8
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
    bestKEYSIZE = 0
    shortestDistance = len(bytesString)
    for KEYSIZE in range(1, min(40, len(bytesString))):
        first = bytesString[:KEYSIZE]
        try:
            second = bytesString[KEYSIZE:2*KEYSIZE]
            third = bytesString[KEYSIZE*2:KEYSIZE*3]
            fourth = bytesString[KEYSIZE*3:KEYSIZE*4]
            fifth = bytesString[KEYSIZE*4:KEYSIZE*5]
            distance1 = hammingDistance(first, second)/KEYSIZE
            distance2 = hammingDistance(first, third)/KEYSIZE
            distance3 = hammingDistance(first, fourth)/KEYSIZE
            distance4 = hammingDistance(second, third)/KEYSIZE
            distance5 = hammingDistance(second, fourth)/KEYSIZE
            distance6 = hammingDistance(third, fourth)/KEYSIZE
            distance7 = hammingDistance(fifth, first)/KEYSIZE
            distance8 = hammingDistance(fifth, second)/KEYSIZE
            distance9 = hammingDistance(fifth, third)/KEYSIZE
            distance10 = hammingDistance(fifth, fourth)/KEYSIZE
            normalizedDistance = (distance1 + distance2 + distance3 + distance4\
            + distance5 + distance6 + distance7 + distance8 + distance9\
            + distance10)/10
        except IndexError:
            try:
                second = bytesString[KEYSIZE:2*KEYSIZE]
                third = bytesString[KEYSIZE*2:KEYSIZE*3]
                fourth = bytesString[KEYSIZE*3:KEYSIZE*4]
                distance1 = hammingDistance(first, second)/KEYSIZE
                distance2 = hammingDistance(first, third)/KEYSIZE
                distance3 = hammingDistance(first, fourth)/KEYSIZE
                distance4 = hammingDistance(second, third)/KEYSIZE
                distance5 = hammingDistance(second, fourth)/KEYSIZE
                distance6 = hammingDistance(third, fourth)/KEYSIZE
                normalizedDistance = (distance1 + distance2 + distance3 + distance4\
                + distance5 + distance6)/6
            except IndexError:
                try:
                    second = bytesString[KEYSIZE:2*KEYSIZE]
                    distance = hammingDistance(first, second)
                    normalizedDistance = distance/KEYSIZE
                except IndexError:
                    second = bytesString[KEYSIZE:]
                    distance = hammingDistance(first, second)
                    normalizedDistance = distance/KEYSIZE
        print(normalizedDistance)
        if normalizedDistance < shortestDistance:
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
        decryption = decryptSingleCharKey(hexstr)
        #key should be a bytes string that looks like b'abc'
        hexStrChar = str(decryption[1])[2:4]
        key += hexStrChar[0].upper()
        key += hexStrChar[1].upper()
    return asciiHexToBytes(key)

