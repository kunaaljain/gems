import os
import sys
import json
import logging
from Crypto.PublicKey import RSA
from django.contrib.auth.models import User
from django.db.models import Q

from models import Users, Candidates,Votes, PublicKeys, ChallengeStrings, Posts, GlobalVariables
import cryptography
import excelfunc

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
	username = []
	for i in range(noUsers):
		challengeStr = cryptography.generateRandomString(128)
		newChallengeStr = ChallengeStrings(challengeStr=challengeStr)
		newChallengeStr.save()

		newPublicKey = addUser(userList[i]['username'], userList[i]['department'], userList[i]['name'], userList[i]['course'], userList[i]['gender'], userList[i]['hostel'], passwords[i])
		username += [userList[i]['username']]
		publicKeys += [newPublicKey]
		user = User.objects.create_user(username = userList[i]['username'], password = passwords[i])
		user.save()
		logger.info('New user added')

	cryptography.permuteList(publicKeys)
	for i in range(len(publicKeys)):
		newPublicKey = PublicKeys(publicKey=publicKeys[i])
		newPublicKey.save()
	excelfunc.passwordtoexcel(passwords=passwords,usernames=username)
	return passwords

def addUser(username, department, name, course, gender, hostel, password, voted=False):
	'''Registers new user with the system including signature key generation and registration'''
	#generate private key
	key = RSA.generate(2048)
	encryptedPrivateKey = cryptography.symmetricEncrypt(key.exportKey(), password)

	p1 = Users(username=username, voted=voted, department=department, name=name, course=course, encryptedPrivateKey=encryptedPrivateKey, gender=gender, hostel=hostel)
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
		voteInfo = "{'totVotes':0, 'courseWise': {'btech': 0, 'mtech': 0, 'phd': 0, 'other': 0, 'prof': 0}, 'genderWise': {'m': 0, 'f':0}, 'departmentWise': {'cs':0, 'ee':0, 'bt':0, 'cl':0, 'ce':0, 'me':0, 'dd':0, 'ma':0, 'ph':0}, 'hostelWise': {'kameng':0, 'barak':0, 'umiam':0, 'manas':0, 'dihing':0, 'bramhaputra':0, 'lohith':0, 'kapili':0, 'siang':0, 'dibang':0, 'dhansiri':0, 'subhansiri':0, 'married-scholars':0}}"
		p1 = Candidates(username=username, details=details, postname=postname, photo=photo, approved=approved, voteInfo='[]')
		p1.save()

		a1 = Agenda(candidate=Users.objects.filter(username=username)[0], content='.')
		a1.save()
		return True

#---------------------------------
def registerVote(plainText, username, password):
	"""Register plainText as the vote of user with given username and password"""
	if GlobalVariables.objects.filter(varname='electionState')[0].value != 'election':
		return False
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
def getVotablePosts(voterGender,voterCourse):
	postsObj = Posts.objects.filter(Q(eligibleGender=voterGender) | Q(eligibleGender='a'))
	postsObj = postsObj.filter(Q(eligibleCourse=voterCourse) | Q(eligibleCourse='a'))
	postsDictList = []
	for item in postsObj:
		postsDictList.append({'postName':item.postname,'postCount':item.postCount,'voterGender':item.eligibleGender,'voterCourse':item.eligibleCourse})
	return postsDictList

#--------------------
def verifyVote():
	"""Verifies all votes"""
	votes = Votes.objects.all()
	text = []
	certi = []
	publickey = []
	verified = []
	result = True
	for vote in votes:
		value = cryptography.asymmetricVerify(vote.plainText, vote.certificate, vote.publicKey.publicKey)
		text += [vote.plainText]
		certi += [vote.certificate]
		publickey += [vote.publicKey.publicKey]
		verified += [result]
		if value == False:
			print error
			result = False

	excelfunc.votestoexcel(text,certi,publickey,verified,result)
	return result

#---------------------
def getStats():
	''' getStats() returns the election stats in the form of a list of tuples in the following format 
	[('Vice President', [('candOne', 400, 'url1')]), 
	('Senator', [('candFive', 500, 'url2'), ('candSix', 764, 'url3'), ('candSeven', 200, 'url4')]),
	('Technical Secratary', [('CandFour', 500, 'url5')])]
	'''
	postsObj = Posts.objects.all()	
	for item in postsObj:
		candStatList = []
		candCount = 0
		candObj = Candidates.objects.all()
		candObj = candObj.filter(contestingPost=postsObj.postName,approved=True)
		for cand in candObj:
			temp = (cand.username,cand.noOfVotes,'permaLink')
			candStatList.append(temp)
		tup = (postsObj.postName,postsObj.postCount, candCount ,candStatList)
		candStatList.append(tup)
	return candStatList

#---------------------

def getWinner(Stats):
	'''This function gets a stats parameter as returned by getStats()
	Returns a list in the same format as getStats() except that 
	it only contains information about the selected candidates
	and omits the second and third item in the tuples 
	eg: [('Vice President', [('candOne', 400, 'url1')]), 
	('Senator', [('candFive', 500, 'url2'), ('candSix', 764, 'url3'), ('candSeven', 200, 'url4')]),
	('Technical Secratary', [('CandFour', 500, 'url5')])]
	'''
	winnerlist = []
	for post in Stats: 
		postwinners = []	
		postwinners = sorted(post[3], key=lambda x: x[1], reverse=True)
		postwinners = postwinners[:post[1]]		#Create a list with the list of selected candidates for the post
		tup = (post[0], postwinners)	#Create the tuple corresponding to the post
		winnerlist.append(tup)		
	return winnerlist
