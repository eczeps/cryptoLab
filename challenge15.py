#15 min

def main(byteString=b"YELLOW SUBMARI\x02\x02", blockSize=16):
    print("stripping " + byteString.decode() + " with block size " + str(blockSize))
    return stripPKCS7(byteString, blockSize)


def stripPKCS7(byteString, blockSize):
    lastByte = byteString[-1]
    if lastByte in bytes(range(blockSize)):
        for i in range(1, lastByte + 1):
            if byteString[-i] != lastByte:
                #invalid PKCS7 padding
                raise ValueError('Invalid PKCS7 padding')
    else:
        #it wasn't padded
        return byteString
    #strip padding and return
    return byteString[:-i]
                