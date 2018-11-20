#1hr

import binascii

def hexTo64(hexstr):
    #convert hex to binary
    binary = binascii.a2b_hex(hexstr)
    #convert binary to base64 and return
    return binascii.b2a_base64(binary)
    
    
def main(hexstr="123456"):
    print("Converting the hex string: ", hexstr)
    result = hexTo64(hexstr)
    print("Binary string: ", result)