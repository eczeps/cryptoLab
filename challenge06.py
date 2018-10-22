#30 min
import binascii
KEYSIZE = 0

def hammingDistance(string1, string2):
    #  ASSUMES THEY'RE THE SAME LENGTH
    ham = 0
    bytes1 = binascii.a2b_qp(string1)
    bytes2 = binascii.a2b_qp(string2)
    for i in range(len(bytes1)):
        bin1 = bin(bytes1[i])
        bin2 = bin(bytes2[i])
        #bin1 and bin2 include an 0b at the beginning -- get rid of it:
        bin1 = bin1[2:]
        bin2 = bin2[2:]
        #bin1 and bin2 will drop any leading 0s, which we need to fix
        bin1 = (8 - len(bin1))*'0' + bin1
        bin2 = (8 - len(bin2))*'0' + bin2
        #now loop through each bit in bins
        for j in range(len(bin1)):
            print(bin1[j], bin2[j])
            if bin1[j] != bin2[j]:
                ham += 1
    return ham