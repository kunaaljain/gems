import os
import sys
import json
from Crypto.PublicKey import RSA

from models import User, Candidates,Votes, PublicKeys, ChallengeStrings
import cryptography

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

	p1 = User(username=username, voted=voted, department=department, name=name, course=course, encryptedPrivateKey=encryptedPrivateKey)
	p1.save()
	return key.publickey().exportKey()

#---------------------------------
def makeCandidate(username, details, photo, approved=False):
	if len(User.objects.filter(username=username)) == 0:
		 return False
	else:
		assert(len(User.objects.filter(username=username)) == 1)
		assert(approved == False)
		assert(len(details) != 0)
		p1 = Candidates(username=username, details=details, photo=photo, approved=approved)
		p1.save()
		return True

#---------------------------------
def registerVote(plainText, username, password):
	"""Register plainText as the vote of user with given username and password"""
	userlist = User.objects.filter(username=username)
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

#---------------------------------
def loginUser(username, password):
	if username =='kayush' and password == 'kayush':
		return True
	else:
		return False

#----------------------------------

def getUserDetails(username):
	details = { 'username':'kayush' , 'voted': True, 'Department':'cse', 'name':'Ayush', 'course':'btech','encryptedPrivateKey':'qwertyuiop' }
	return details

#-------------------------------

def validateAllVotes():
	validate = ['True','True' , 'False']
	return validate

#-----------------------

def getElectionStats():
	Stats = {'vote-count':{'candidate1':100, 'candidate2':97},'vote-turnout':0.67, 'vote-demographics':{'btech':0.4,'mtech':0.5, 'dual':0.1}}
	return Stats

#--------------------
def getWinner(Stats):
	return 'Candidate1'
#-------------------

def approveCandidate(username):
	if username == 'sudhanshu':
		return True
	else:
		return False

#------------------------

def getCandidateDetail(username):
	details = {'username':'sudhanshu', 'post':'vp', 'picture':'sudhanshu.jpg','form-data':{'agenda':'my agenda', 'position-of-responsibility':'Director of IITG' }}
	return details

#----------------------

def setCandidateDetails(username):
	detail = getCandidateDetail(username);
	# converting dict to json
	detail = json.dumps(detail)
	return detail
#----------------------
def getElectionState(state):
	if state == 0:
		var = 'pre-election'
	elif state == 1:
		var = 'during election'
	else:
		var = 'post-election'
	return var
#-----------------------------
def setElectionState(state):
    if state == 0:
        var = 'pre-election'
    elif state == 1:
        var = 'during election'
    else:
        var = 'post-election'
#-------------------------
def getCandidatePost(postId):
	post = {'vp':{'candidate1':'Ayush ', 'Candidate2':'Sudhanshu'}, 'welfare':{'candidate1':'Ayush ', 'Candidate2':'Sudhanshu'}, 'sport':{'candidate1':'Ayush ', 'Candidate2':'Sudhanshu'}}
	return post

#--------------------------
def importElectionData(src):
	stats = {'':''}
	return stats
#------------------------
def verifyVote(votes):
	"""Verifies all votes"""
	for vote in votes:
		value = cryptography.asymmetricVerify(vote.plainText, vote.certificate, vote.publicKey.publicKey)
		if value == False:
			print error
			return value
	return value
