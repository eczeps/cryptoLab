#5.5 hrs (also refining challenge 3)
#NOTE: MAKE SURE THAT YOU'VE SYNCED DIRECTORY TO THE EDITOR (BOTTOM RIGHT IN CANOPY)

from challenge03 import *

def main(filename):
    listOfCiphertexts = parseFile(filename)
    listOfPlaintexts = [decrypt(ciphertext) for ciphertext in listOfCiphertexts]
    print(listOfPlaintexts)
    bestGuess = pickPlaintext(listOfPlaintexts)
    return bestGuess
    
#given a filename, parses and on each newline adds the string to a list
def parseFile(filename):
    result = []
    with open(filename, 'r') as textfile:
        for line in textfile:
            result.append(line)
    return result
