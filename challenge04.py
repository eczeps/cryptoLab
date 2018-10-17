#2 hrs

from challenge03 import *

def main(filename):
    listOfCiphertexts = parseFile(filename)
    print(listOfCiphertexts)
    listOfPlaintexts = [decrypt(ciphertext) for ciphertext in listOfCiphertexts]
    print(listOfPlaintexts)
    return pickPlaintext(listOfPlaintexts)
    
#given a filename, parses and on each newline adds the string to a list
def parseFile(filename):
    result = ['1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736', '65656565', '2727272727']
    return result
