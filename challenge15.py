#15 min


def stripPKCS7(byteString, blockSize):
    lastByte = byteString[-1]
    #assumes block size of 16
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
                