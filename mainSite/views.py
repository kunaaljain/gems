#import field dependencies
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader,Template,Context
from .databaseManager import getCandidateDetail,getCandidatesList

#import database fields
from mainSite.models import User, Candidates,Votes, PublicKeys, ChallengeStrings , Posts

# Create your views here.
def resultsView(request):
	indexPage = loader.get_template('index.html')
	
	stats = [	('vp',1,2,	[ ('candOne',200,'permaLink'),('candTwo',300,'xxx') ]	) ,
				('tech',1,2,[ ('candThree',400,'xxx') , ('candFour',500,'xxx')]),
				('welfare',1,3,[('candFive',500,'xxx') , ('candSix',764,'xxx') , ('candSeven',200,'xxx')])
			]
	NoOfVotes = 1000
	contextObj = Context({'stats':stats,'NoOfVotes':NoOfVotes})

	return render_to_response('results.html',contextObj)
	#return HttpResponse("index.html")
def candidateStat(request,candidateName):
	deptStats = {('cse',35),('ece',56)}
	courseStats = {('ug',55),('pg',26),('phd',33)}
	hostelStats = {('umiam',33),('kameng',55),('barak',24)}
	contextObj =Context({'candidatename':candidateName,'deptStats':deptStats,'courseStats':courseStats,'hostelStats':hostelStats})
	return render_to_response('candidateStats.html',contextObj)

def candidateView(request,candidateName):
	candidateDetails = getCandidateDetail(candidateName)
	contextObj = Context({'candidateName':candidateName,'candidateDetails':candidateDetails})
	return render_to_response('test.html',contextObj)

def candidatesListView(request):
	
	candidatesList = getCandidatesList()
	contextObj = Context({'candidatesList':candidatesList})
	return render_to_response('candidates.html',contextObj)