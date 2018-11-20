#6 hrs, mostly refining challenge 3 scoring function and remembering the key that worked

from challenge03 import *

def main(filename="4.txt"):
    print("decrypting ciphertext in file " + filename)
    listOfCiphertexts = parseFile(filename)
    listOfPlaintexts = [decryptSingleCharKey(ciphertext) for ciphertext in listOfCiphertexts]
    bestGuess = pickPlaintext(listOfPlaintexts)
    return bestGuess[0][0]
    
#given a filename, parses and on each newline adds the string to a list
def parseFile(filename):
    result = []
    with open(filename, 'r') as textfile:
        for line in textfile:
            result.append(line)
    return result
