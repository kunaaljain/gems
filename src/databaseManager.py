#this is the dummy database connecting python file for helping the UI/UX guys
#~/bin/kayush/python/databaseManager.py
import os,sys
import json

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
	else
		return True

#----------------------------------

def getUserDetails(username):
	details = { 'username':'kayush' , 'voted': True, 'Department':'cse', 'name':'Ayush', 'course':'btech'}
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
def getElectionState():
	state = 0 #modify as per requirement of module
	if state ==0:
		var = 'pre-election'
	elif state == 1:
		var = 'during-election'
	else:
		var = 'post-election'
	return var
#-----------------------------
def setElectionState(state):
        if state == 'pre-election:
                var = 0
        elif state == 'during-election':
                var = 1
        else:
                var = 2
		assert(state == 'post-election')
#-------------------------
def getCandidatePost(postId):
	post = {'vp':{'candidate1':'kayush ', 'Candidate2':'sudhanshu'}, 'welfare':{'candidate1':'kayush ', 'Candidate2':'sudhanshu'}, 'sport':{'candidate1':'kayush ', 'Candidate2':'sudhanshu'}}
	return post

#--------------------------
def getElectionStats(src):
	stats = {'':''}
	return stats
#------------------------
	
