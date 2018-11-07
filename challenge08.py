#3.5 hrs; most of it spent fixing challenge06

def main(filename):
    listOfCiphertexts = parseFile(filename)
    likelyEncrypted = findLikelyEncrypted(listOfCiphertexts)
    return likelyEncrypted
    
#given a filename, parses and on each newline adds the string to a list
def parseFile(filename):
    result = []
    with open(filename, 'r') as textfile:
        for line in textfile:
            result.append(bytes.fromhex(line[:-1]))
    return result

    
    
def findLikelyEncrypted(listOfCiphertexts):
    #we'll look through each ciphertext and see if any of its 16 byte blocks repeat
    #taking the set of a list removes duplicates, given that elts are hashable
    repeatList = []
    for ciphertext in listOfCiphertexts:
        repeatList.append(numRepeatedBlocks(ciphertext))
    bestGuessIndex = repeatList.index(max(repeatList))
    bestGuess = listOfCiphertexts[bestGuessIndex]
    return bestGuess
    
    
    
    
def numRepeatedBlocks(ciphertext):
    #make a list of each 16 byte block:
    #this is a less strict way of doing it, but it works for this exercise
    #blockList = [ciphertext[16*i:16*(i+1)] for i in range(0, int(len(ciphertext)/16))]
    #use this if results stop being precise enough
    blockList = [ciphertext[i: i + 16] for i in range(0, len(ciphertext) - 15)]
    duplicates = 0
    seen = []
    for i in range(len(blockList)):
        if blockList[i] not in seen:
            seen.append(blockList[i])
        else:
            duplicates += 1
    return duplicates