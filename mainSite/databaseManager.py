import os
import sys
import json
import logging
from Crypto.PublicKey import RSA
from django.contrib.auth.models import User

from models import Users, Candidates,Votes, PublicKeys, ChallengeStrings
import cryptography

logger = logging.getLogger(__name__)

def registerUsers(userList):
	"""Registers a new set of users as specified in userList.

	Should be called with a large number of users for good security (prefferably all that will ever be in the system.)

	userList -- list of dictionaries each depicting a user with the keys:
		'username', 'department', 'name', 'course'

	returns a list of passwords corresponding to each user
	"""

	noUsers = len(userList)
	passwords = [cryptography.generatePrintableRandomString() for i in range(noUsers)]

	publicKeys = []
	for i in range(noUsers):
		challengeStr = cryptography.generateRandomString(128)
		newChallengeStr = ChallengeStrings(challengeStr=challengeStr)
		newChallengeStr.save()

		newPublicKey = addUser(userList[i]['username'], userList[i]['department'], userList[i]['name'], userList[i]['course'], passwords[i])

		publicKeys += [newPublicKey]
		user = User.objects.create_user(username = userList[i]['username'], password = passwords[i])
		user.save()
		logger.info('New user added')

	cryptography.permuteList(publicKeys)
	for i in range(len(publicKeys)):
		newPublicKey = PublicKeys(publicKey=publicKeys[i])
		newPublicKey.save()

	return passwords

def addUser(username, department, name, course, password, voted=False):
	'''Registers new user with the system including signature key generation and registration'''
	#generate private key
	key = RSA.generate(2048)
	encryptedPrivateKey = cryptography.symmetricEncrypt(key.exportKey(), password)

	p1 = Users(username=username, voted=voted, department=department, name=name, course=course, encryptedPrivateKey=encryptedPrivateKey)
	p1.save()
	return key.publickey().exportKey()

#---------------------------------
def makeCandidate(username, details, postname, photo, approved=False):
	# if GlobalVariables.objects.filter(varname='electionState') != 'pre-election':
	# 	return False
	if len(Users.objects.filter(username=username)) == 0:
		 return False
	else:
		assert(len(Users.objects.filter(username=username)) == 1)
		#assert(approved == False)
		assert(len(details) != 0)
		p1 = Candidates(username=username, details=details, postname=postname, photo=photo, approved=approved)
		p1.save()

		a1 = Agenda(candidate=Users.objects.filter(username=username)[0], content='.')
		return True

#---------------------------------
def registerVote(plainText, username, password):
	"""Register plainText as the vote of user with given username and password"""
	# if GlobalVariables.objects.filter(varname='electionState') != 'election':
	# 	return False
	userlist = Users.objects.filter(username=username)
	#print len(userlist)
	if (len(userlist) == 0):
		return False
	assert(len(userlist) == 1)
	decryptedPrivateKey = cryptography.symmetricDecrypt(userlist[0].encryptedPrivateKey,password)

	certificate = cryptography.asymmetricSign(plainText,decryptedPrivateKey)
	key = RSA.importKey(decryptedPrivateKey)
	key = key.publickey().exportKey()
	assert(len(PublicKeys.objects.filter(publicKey=key)) == 1)
	publicKey = PublicKeys.objects.filter(publicKey=key)[0]

	challenobj = ChallengeStrings.objects.all()
	lenofcha = len(challenobj)
	rannum = lenofcha/2
	'''get a random number'''
	p1 = Votes(plainText=plainText, certificate=certificate, publicKey=publicKey, challengeStr = challenobj[rannum])
	p1.save()
	return True

#--------------------
def setCandidateDetails(username):
	detail = getCandidateDetail(username);
	# converting dict to json
	detail = json.dumps(detail)
	return detail

#--------------------
def verifyVote(votes):
	"""Verifies all votes"""
	for vote in votes:
		value = cryptography.asymmetricVerify(vote.plainText, vote.certificate, vote.publicKey.publicKey)
		if value == False:
			print error
			return value
	return value
