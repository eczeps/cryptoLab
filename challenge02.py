#1hr
import binascii

def fixed_XOR(hexstr1, hexstr2):
    return hex(int(hexstr1, 16) ^ int(hexstr2, 16))