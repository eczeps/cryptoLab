#4.5 hrs

def main(ciphertext):
    allPlaintexts = getAllPlaintexts(ciphertext)
    listOfFrequencyDicts = [getFrequencyDict(plaintext) for plaintext in allPlaintexts]
    listOfScores = [scoreFrequencyDict(freqDict) for freqDict in listOfFrequencyDicts]
    bestGuessIndex = listOfScores.index(max(listOfScores))
    bestGuess = allPlaintexts[bestGuessIndex]
    #convert bestGuess to printable ascii characters
    return bytes.fromhex(bestGuess[2:])

#generate a list of all possible plaintexts, still in hex
def getAllPlaintexts(ciphertext):
    result = []
    #just generating a list of all the possible bytes:
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    keyBytes = [a + b for b in digits for a in digits]
    #how many times you have to repeat each key char to make it the length of ciphertext
    length = int(len(ciphertext)/2)
    allKeys = [byte*length for byte in keyBytes]
    for key in allKeys:
        hexXOR = fixed_XOR(ciphertext, key)
        result.append(hexXOR)
    return result

#from challenge2
def fixed_XOR(hexstr1, hexstr2):
    return hex(int(hexstr1, 16) ^ int(hexstr2, 16))
    
    
#returns frequency dict of each byte in plaintext, converted to decimal
def getFrequencyDict(plaintext):
    plaintext = plaintext[2:]
    result = {}
    #this makes a list of bytes in DECIMAL
    try:
        listOfBytes = list(bytes.fromhex(plaintext))
    except ValueError:
        #sometimes it shaves off the last 0 of plaintext, and then this throws an error
        listOfBytes = list(bytes.fromhex(plaintext + '0'))
    for byte in listOfBytes:
        if byte not in result.keys():
            result[byte] = 1
        else:
            result[byte] +=1
    return result
    
def scoreFrequencyDict(frequencyDict):
    score = 0
    
    #discard dict if it has nonprintable chars:
    keys = frequencyDict.keys()
    for i in range(31):
        if i in keys:
            return -1000
    #more nonprintable char checking:
    for i in range(128, 255):
        if i in keys:
            return -1000
            
    
    inverse = [(value, key) for key, value in frequencyDict.items()]
    sorted_by_value = sorted(inverse, key=lambda tup: tup[0])
    #can play around with the indices we use from sorted_by_value
    mostCommon = [elt[1] for elt in sorted_by_value[-6:-1]]
    #if it's an E or e
    if 69 in mostCommon or 101 in mostCommon:
        score += 13
    #if it's T or t
    if 84 in mostCommon or 116 in mostCommon:
        score += 12
    #if it's A or a
    if 65 in mostCommon or 97 in mostCommon:
        score +=11
    if 79 in mostCommon or 111 in mostCommon:
        score +=10
    if 73 in mostCommon or 105 in mostCommon:
        score +=9
    if 78 in mostCommon or 110 in mostCommon:
        score +=8
    if 83 in mostCommon or 115 in mostCommon:
        score +=7
    if 82 in mostCommon or 114 in mostCommon:
        score +=6
    if 72 in mostCommon or 104 in mostCommon:
        score +=5
    if 76 in mostCommon or 108 in mostCommon:
        score +=4
    if 67 in mostCommon or 99 in mostCommon:
        score +=3
    if 85 in mostCommon or 117 in mostCommon:
        score +=2
    #######################################
    if 77 in mostCommon or 109 in mostCommon:
        score -= 1
    if 70 in mostCommon or 102 in mostCommon:
        score -= 2
    if 80 in mostCommon or 112 in mostCommon:
        score -= 3
    if 71 in mostCommon or 103 in mostCommon:
        score -= 4
    if 87 in mostCommon or 119 in mostCommon:
        score -= 5
    if 89 in mostCommon or 121 in mostCommon:
        score -= 6
    if 66 in mostCommon or 98 in mostCommon:
        score -= 7
    if 86 in mostCommon or 118 in mostCommon:
        score -= 8
    if 75 in mostCommon or 107 in mostCommon:
        score -= 9
    if 88 in mostCommon or 120 in mostCommon:
        score -= 10
    if 74 in mostCommon or 106 in mostCommon:
        score -= 11
    if 81 in mostCommon or 113 in mostCommon:
        score -= 12
    if 90 in mostCommon or 122 in mostCommon:
        score -= 13
    #if it's J or j
    if 74 in mostCommon or 106 in mostCommon:
        score -= 11
    #if it's Q or q
    if 81 in mostCommon or 113 in mostCommon:
        score -= 12
    #if it's Z or z
    if 90 in mostCommon or 122 in mostCommon:
        score -= 13
    return score