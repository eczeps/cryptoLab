from challenge03 import *

def main(filename):
    listOfCiphertexts = parseFile(filename)
    listOfPlaintexts = [bytes.hex(decrypt(ciphertext)) for ciphertext in listOfCiphertexts]
    print(listOfPlaintexts)
    return pickPlaintext(listOfPlaintexts)
    
#given a filename, parses and on each newline adds the string to a list
def parseFile(filename):
    result = ['45']
    return result
