from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA
from Crypto import Random
from Crypto.PublicKey import RSA
import binascii

'''---------------The Encryption Abstraction----------------'''

constPadString = u"dkgh;slfdkgukrjfdkgh;slfdkgukrjf"
def preprocessString(inpString): #pad to length of size 32
	return (inpString + u"$" + constPadString)[:32]

def unpreprocessString(inpString):
	for i in range(len(inpString)):
		if inpString[i] == '$':
			break
	return inpString[:i]


AESInitializationVector = "jhfdiyeqkjxjvgljdfhsdkjghdsflcgf"[:16]
def symmetricEncrypt(inpString, key):
	cipher = AES.new(preprocessString(key), AES.MODE_CFB, AESInitializationVector)
	msg = AESInitializationVector + cipher.encrypt(inpString)
	return binascii.b2a_base64(msg)

def symmetricDecrypt(inpString, key):
	inpString = binascii.a2b_base64(inpString)
	cipher = AES.new(preprocessString(key), AES.MODE_CFB, AESInitializationVector)
	msg = cipher.decrypt(inpString)
	return msg[16:]

def asymmetricPublicEncrypt(inpString, key):	
	symKey = binascii.b2a_base64(Random.new().read(128))
	cipher = PKCS1_OAEP.new(RSA.importKey(key))
	ct = binascii.b2a_base64(cipher.encrypt(symKey)) + symmetricEncrypt(inpString, symKey)
	#print len(binascii.b2a_base64(cipher.encrypt(symKey))), ct
	return ct

def asymmetricPrivateDecrypt(inpString, key):
	cipher = PKCS1_OAEP.new(RSA.importKey(key))
	#print inpString[:345]
	symKey = cipher.decrypt(binascii.a2b_base64(inpString[:345]))
	return symmetricDecrypt(inpString[345:], symKey)

maxRSAPlaintextLength = 128 #RSA cannot be used to encrypt plaintexts longer than this
maxRSACiphertextLength = 345 #Given largest feasible plaintext, this is the length of the ciphertext

def asymmetricSign(message, key):
	"""Returns a signature of inpString signed with 'key'."""
	key = RSA.importKey(key)	
	h = SHA.new()
	h.update(message)
	signer = PKCS1_PSS.new(key)
	return binascii.b2a_base64(signer.sign(h))

def asymmetricVerify(message, signature, key):
	"""Verifies the signature using 'key' and 'message'"""
	key = RSA.importKey(key)
	h = SHA.new()
	h.update(message)
	verifier = PKCS1_PSS.new(key)
	signature = binascii.a2b_base64(signature)
	return verifier.verify(h, signature)

'''
#Test code for this module. Uncomment to test
key = RSA.generate(2048)
certificate = asymmetricSign("Hello world", key.exportKey())
print len(certificate)
print asymmetricVerify("Hello world", certificate, key.publickey().exportKey())

c = asymmetricPublicEncrypt("Hello World", key.publickey().exportKey())
asymmetricPrivateDecrypt(c, key.exportKey())
'''
