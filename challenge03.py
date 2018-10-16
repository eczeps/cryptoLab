#2 hrs
import binascii
import string
import codecs
decode_hex = codecs.getdecoder("hex_codec")


def main(ciphertext):
    allPlaintexts = getAllPlaintexts(ciphertext)
    listOfFrequencyDicts = [getFrequencyDict(plaintext) for plaintext in allPlaintexts]
    

#generate a list of all possible plaintexts
def getAllPlaintexts(ciphertext):
    result = []
    #change this later
    characters = 'abcd'
    #hexCharacters = binascii.b2a_hex(binascii.a2b_base64(characters))
    print(characters)
    #how many times you have to repeat each key char to make it the length of ciphertext
    length = int(len(ciphertext))
    allKeys = [s*length for s in characters]
    print(allKeys)
    for key in allKeys:
        hexXOR = fixed_XOR(ciphertext, key)
        result.append(hexXOR)
    return result

#from challenge2
def fixed_XOR(hexstr1, hexstr2):
    return hex(int(hexstr1, 16) ^ int(hexstr2, 16))
    
def getFrequencyDict(plaintext):
    print(plaintext)
    result = {}
    listOfBytes = list(bytes.fromhex(plaintext))
    for byte in listOfBytes:
        if byte not in result.keys():
            result[byte] = 1
        else:
            result[byte] +=1
    return result