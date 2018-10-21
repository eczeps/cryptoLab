#6 hrs (mostly refining challenge 3)
#NOTE: MAKE SURE THAT YOU'VE SYNCED DIRECTORY TO THE EDITOR (BOTTOM RIGHT IN CANOPY)

from challenge03 import *
import pprint

def main(filename):
    listOfCiphertexts = parseFile(filename)
    #check that you're parsing the file right
    pprint.pprint(listOfCiphertexts)
    #check the type of a ciphertext against what decrypt is expecting
    listOfPlaintexts = [decrypt(ciphertext) for ciphertext in listOfCiphertexts]
    #print(listOfPlaintexts)
    bestGuess = pickPlaintext(listOfPlaintexts)
    return bestGuess
    
#given a filename, parses and on each newline adds the string to a list
def parseFile(filename):
    result = []
    with open(filename, 'r') as textfile:
        for line in textfile:
            result.append(line)
    return result
