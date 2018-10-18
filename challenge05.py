#1 hr

import math



def main(plaintext, key):
    #key is a string, plaintext is bytes
    return encrypt(plaintext.encode(), key)

#returns a key in BYTES
def generateKey(plaintext, key):
    length = len(plaintext)
    #this is the key repeated all the times its repeated fully. i.e. ICE not ICEI
    shortkey = key*(int((length/len(key))))
    mod = length%len(key)
    #adds the part that didn't divide evenly
    fullkey = shortkey + key[:mod]
    '''TO DO LATER:
    CONVERT FULLKEY TO HEX FROM STRING BEFORE ENCODING
    '''
    return fullkey.encode()
    
#both arguments should be in BYTES
def encrypt(plaintext, key):
    bytesKey = generateKey(plaintext, key)
    XOR = fixed_xor(plaintext, bytesKey)
    return XOR
    

def fixed_xor(plaintext, key):
    print(bytes.hex(plaintext))
    print(key)
    intXOR = int(bytes.hex(plaintext), 16) ^ int(bytes.hex(key), 16)
    hexXOR = hex(intXOR)
    try:
        return bytes.fromhex(hexXOR[2:])
    except ValueError or TypeError:
        return bytes.fromhex('0' + hexXOR[2:])