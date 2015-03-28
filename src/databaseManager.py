#this is the dummy database connecting python file for helping the UI/UX guys
#~/bin/kayush/python/databaseManager.py
import os,sys
import json

from models import User, Candidates,Votes, PublicKeys, ChallengeStrings 
 

def addUser(username,voted,department,name,course,encryptedPrivateKey):
	p1 = User(username=username, voted=voted, department=department, name=name, course=course, encryptedPrivateKey=encryptedPrivateKey)
	p1.save()
	return True

#---------------------------------
def addCandidate(username,details,photo,approved):
	if len(User.objects.all()) == 0:
		 return False
	else:
		p1 = Candidates(username=username, details=details, photo=photo, approved=approved)
		p1.save()
		return True
#---------------------------------
def addVotes(plainText,certificate):
	p1 = Votes(plainText=plainText, certificate=certificate)
	p1.save()
#--------------------------------
def addChallengeStrings(challengeStr):
	p1 = ChallengeStrings(challengeStr=challengeStr)
	p1.save()
#---------------------------------
def addPublicKeys(publicKey):
	p1 = PublicKeys(publicKey=publicKey)
	p1.save()
#---------------------------------
def loginUser(username, password):
	if username =='kayush' and password == 'kayush':
		return True
	else:
		return False
#----------------------------------
def registerVote(username,vote):
	decoded = json.loads(vote)
	var1 = decoded['vp']
	var2 = decoded['welfare']
	var3 = decoded['sport']
	# by default i assign the value false to vated although it will come from database
	voted = False
	if voted != False:
		return False
	else:
		return True

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
	detail = {'username':'sudhanshu', 'post':'vp', 'picture':'sudhanshu.jpg','form-data':{'agenda':'my agenda', 'position-of-responsibility':'Director of IITG' }}
	return details

#----------------------

def setCandidateDetails(username):
	detail = getCandidateDetail(username);
	# converting dict to json 
	detail = json.dumps(detail)
	return detail
#----------------------
def getElectionState(state):
	if state ==0:
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
