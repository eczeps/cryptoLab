#some time
from challenge04 import parseFile

def main(filename):
    listOfCiphertexts = parseFile(filename)
    likelyEncrypted = findLikelyEncrypted(listOfCiphertexts)
    return 