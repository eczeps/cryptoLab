#30 min
import binascii

def hammingDistance(string1, string2):
    #  assumes string1 >= string2
    ham = 0
    bytes1 = binascii.a2b_qp(string1)
    bytes2 = binascii.a2b_qp(string2)
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
        print(ham)
        print(len(string1) - len(string2))
        #8 bits per byte, char is 2 bytes, so we multiply by 4
        ham += (len(string1) - len(string2))*4
    return ham
    
def findKeySize(bytesString):
    #think real hard if this should take a string or bytes
    bestKEYSIZE = 0
    shortestDistance = len(bytesString)
    for KEYSIZE in range(2, min(40, len(bytesString) -1)):
        first = bytesString[:KEYSIZE]
        print(first)
        try:
            second = bytesString[KEYSIZE:2*KEYSIZE]
            print(second)
        except IndexError:
            second = bytesString[KEYSIZE:]
        distance = hammingDistance(first, second)
        normalizedDistance = distance/KEYSIZE
        if normalizedDistance < shortestDistance:
            shortestDistance = normalizedDistance
            bestKEYSIZE = KEYSIZE
    return bestKEYSIZE