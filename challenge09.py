#20 min

def PKCS7pad(plaintext, targetLen):
    #targetLen must be >= len(plaintext)
    #plaintext should be bytes, like b"YELLOW SUBMARINE"
    #targetLen should be an int
    length = len(plaintext)
    difference = targetLen - length
    return plaintext + bytes([difference])*difference