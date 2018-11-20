#20 min


def main(plaintext=b"hello", targetLen=16):
    print("padding plaintext " + plaintext.decode() + " to length " + str(targetLen))
    result = PKCS7pad(plaintext, targetLen)
    return result

def PKCS7pad(plaintext, targetLen):
    #targetLen must be >= len(plaintext)
    #plaintext should be bytes, like b"YELLOW SUBMARINE"
    #targetLen should be an int
    length = len(plaintext)
    difference = targetLen - length
    return plaintext + bytes([difference])*difference