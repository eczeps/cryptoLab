#3.5 hrs
#this took an extra like 2 hours because i wasn't including the newline in the plaintext

def main(plaintext="Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal", key="ICE"):
    encryption = encrypt(plaintext.encode(), key)
    return bytes.hex(encryption)

#returns a key in BYTES
def generateKey(plaintext, key):
    length = len(plaintext)
    #this is the key repeated all the times its repeated fully. i.e. ICE not ICEI
    shortkey = key*(int((length/len(key))))
    mod = length%len(key)
    #adds the part that didn't divide evenly
    fullkey = shortkey + key[:mod]
    finalkey = ""
    #convert string to hex string:
    for c in fullkey:
        #get the hex string version of the char
        intchar = ord(c)
        hexchar = hex(intchar)
        #add it to our key
        finalkey += hexchar[2:]
    #if you want the hex encoding of the ascii char values, return finalkey.encode()
    return fullkey.encode()
    
#both arguments should be in BYTES
def encrypt(plaintext, key):
    bytesKey = generateKey(plaintext, key)
    XOR = fixed_xor(plaintext, bytesKey)
    return XOR
    

def fixed_xor(plaintext, key):
    intXOR = int(bytes.hex(plaintext), 16) ^ int(bytes.hex(key), 16)
    hexXOR = hex(intXOR)
    try:
        return bytes.fromhex(hexXOR[2:])
    except ValueError or TypeError:
        return bytes.fromhex('0' + hexXOR[2:])