#1


'''TO RUN THIS FILE:
either just run main, or:
as the attacker, run attack()
as a good person making an account, run profile_for() for unencrypted, or 
getEncryptedProfile() for encrypted
'''



from challenge11 import random16Bytes, next16Multiple
from challenge10 import AESencrypt, AESdecrypt
from challenge09 import PKCS7pad
from challenge15 import stripPKCS7

KEY = random16Bytes()


def main(email=b"hello@abc.com"):
    print("creating an account as a non-adversary for email " + email.decode())
    goodProf = profile_for(email)
    print(goodProf)
    print("attacking!")
    return attack()
    


def attack(BLOCKSIZE=16):
    evil1 = getEncryptedProfile(b"admin")
    evil2 = getEncryptedProfile(b"normalEmail@everythingisok.com")
    decryptedEvil1 = stripPKCS7(decryptUserProfile(evil1), BLOCKSIZE)
    decryptedEvil2 = stripPKCS7(decryptUserProfile(evil2), BLOCKSIZE)
    sploit = decryptedEvil2[:-5] + decryptedEvil1[5:11]
    return sploit
    
    

def getEncryptedProfile(email):
    return encryptUserProfile(profile_for(email))


def profile_for(email):
    cleanedEmail = cleanEmail(email)
    uid = b"10"
    result = b"email=" + cleanedEmail + b"&uid=" + uid + b"&role=user"
    return result
    
    
def cleanEmail(email):
    result = b""
    for char in email:
        if char != b"&" and char != b"=":
            result += bytes([char])
    return result
    
def encodeDict(userDict):
    #dict to bytestring
    result = b""
    for key in userDict.keys():
        result+= key + b"=" + userDict[key] + b"&"
    return result[:-1]
    
    
def parseStructuredCookie(string):
    #string to dict
    result = {}
    keyvals = string.split('&')
    for keyval in keyvals:
        tup = keyval.split('=')
        result[tup[0]] = tup[1]
    return result
    
    
#create this profile by getting two or more ciphertexts and splitting them up and gluing them together
#create a profile that's an encrypted ciphertext that when decrypted and parsed will have admin role

#overall approach: get one thing with the email as admin, and the put it on another thing
#evil string1: email=admin&uid=10&role=user
#evil string2: email=normalemail&uid=10&role=user
#exploit string: string2[:-4] + string1[5:10]

def encryptUserProfile(string):
    byteString = string###################
    targetLen = next16Multiple(len(byteString))
    paddedPlaintext = PKCS7pad(byteString, targetLen)
    ciphertext = AESencrypt(paddedPlaintext, KEY)
    return ciphertext
    
def decryptUserProfile(ciphertext):
    ciphertext = ciphertext #################
    targetLen = next16Multiple(len(ciphertext))
    paddedCiphertext = PKCS7pad(ciphertext, targetLen)
    plaintext = AESdecrypt(paddedCiphertext, KEY)
    return plaintext