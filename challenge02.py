#1hr
import binascii

def fixed_XOR(hexstr1, hexstr2):
    return hex(int(hexstr1, 16) ^ int(hexstr2, 16))
    
    
def main(hexstr1="12", hexstr2="34"):
    print("XORing the strings " + hexstr1 + " and " + hexstr2)
    result = fixed_XOR(hexstr1, hexstr2)
    print("result:", result)