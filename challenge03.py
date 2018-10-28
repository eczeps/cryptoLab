#5.5 hrs




def main(ciphertext):
    return decryptSingleCharKey(ciphertext)

def decryptSingleCharKey(ciphertext):
    allPlaintexts = getAllPlaintexts(ciphertext)
    bestPlaintext = pickPlaintext(allPlaintexts)
    return (bestPlaintext[0])
    

#generate a list of all possible plaintexts, still in bytes
def getAllPlaintexts(ciphertext):
    result = []
    #just generating a list of all the possible bytes:
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    keyBytes = [a + b for a in digits for b in digits]
    #keyBytes = ['61']
    #keyBytes = [x for x in range(0xFF+1)]
    #how many times you have to repeat each key char to make it the length of ciphertext
    length = int(len(ciphertext)/2)
    allKeys = [(byte*length).encode() for byte in keyBytes]
    for key in allKeys:
        bytesXOR = fixed_XOR(ciphertext, key)
        result.append((bytesXOR, key))
    return result

#edited!! different from the one in challenge2
def fixed_XOR(hexstr1, hexstr2):
    intXOR = int(hexstr1, 16) ^ int(hexstr2, 16)
    hexXOR = hex(intXOR)
    try:
        return bytes.fromhex(hexXOR[2:])
    except ValueError or TypeError:
        return bytes.fromhex('0' + hexXOR[2:])
        
    
#given a list of plaintexts in bytes, return the most likely one still in bytes
def pickPlaintext(allPlaintexts):
    '''
    listOfFrequencyDicts = [getFrequencyDict(plaintext) for plaintext in allPlaintexts]
    listOfScores = [scoreFrequencyDict(freqDict) for freqDict in listOfFrequencyDicts]
    zipped = list(zip(listOfScores, allPlaintexts))
    filtered = [entry for entry in zipped if entry[0] > 0]
    pprint.pprint(filtered)
    '''
    listOfScores = [scorePlaintext(plaintext[0]) for plaintext in allPlaintexts]
    zipped = list(zip(listOfScores, allPlaintexts[0]))
    filtered = [entry for entry in zipped if entry[0] > 50]
    #pprint.pprint(filtered)
    bestGuessIndex = listOfScores.index(max(listOfScores))
    bestGuess = allPlaintexts[bestGuessIndex]
    return (bestGuess, bestGuessIndex)

    
#returns frequency dict of each byte in plaintext, converted to decimal
#tbh not sure where the conversion happens, but key values end up in decimal
def getFrequencyDict(plaintext):
    result = {}
    #this makes a list of bytes in DECIMAL
    try:
        listOfBytes = list(plaintext)
    except ValueError:
        #sometimes it shaves off the last 0 of plaintext, and then this throws an error
        listOfBytes = list('0' + plaintext)
    for byte in listOfBytes:
        if byte not in result.keys():
            result[byte] = 1
        else:
            result[byte] +=1
    return result
    
    
def scorePlaintext(plaintext):
    score = 0
    scoresDict = {b'e': 13, b'E': 13,
                    b't': 12, b'T': 12,
                    b'a': 11, b'A': 11,
                    b'o': 10, b'O': 10,
                    b'i': 9, b'I': 9,
                    b's': 8, b'S': 8,
                    b'r': 7, b'R': 7,
                    b'h': 6, b'H': 6,
                    b'l': 5, b'L': 5,
                    b'd': 4, b'D': 4,
                    b'c': 3, b'C': 3,
                    b'u': 2, b'U': 2,
                    b'm': 1, b'M': 1,
                    b'f': -1, b'F': -1,
                    b'p': -2, b'P': -2,
                    b'g': -3, b'G': -3,
                    b'w': -4, b'W': -4,
                    b'y': -5, b'Y': -5,
                    b'b': -6, b'B': -6,
                    b'v': -7, b'V': -7,
                    b'k': -8, b'K': -8,
                    b'x': -9, b'X': -9,
                    b'j': -10, b'J': -10,
                    b'q': -11, b'Q': -11,
                    b'z': -12, b'Z': -12,
                    }
    for char in plaintext:
        char = bytes([char])
        if char == b' ':
            score += 100
        else:
            score += scoresDict.get(char, 0)
    return score
    