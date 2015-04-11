from django.shortcuts import render_to_response, render ,get_list_or_404, get_object_or_404
from mainSite.models import *
import json
from django.http import HttpResponse
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from .databaseManager import getCandidateDetail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user

from mainSite.models import Agenda,Comments,CommentLikes
from mainSite.forms import CommentForm


def user_login(request):                      #url for login page is home/login
    if request.method == 'POST':
    	username= request.POST.get('username')
    	password = request.POST.get('password')
    	user = authenticate(username=username,password=password)
    	if user:
    	    if (user.is_active and user.is_staff):
    	        login(request, user)
    	        return HttpResponseRedirect('/gems/admin')
    	    else:
                login(request, user)
                return HttpResponseRedirect('/gems/voterHome')
    	else:
    	    return HttpResponse("your account is diabled")		
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html', {})		
    return render(request, 'index.html', context_dict)

@login_required
def voterHome(request):
	return render(request, 'main_page.html')

def view_candidate(request):
    	candidate_i = New_Candidate.objects.all()
	candidate_data = {
		"candidate_detail" : candidate_i
	}
	return render_to_response('view_candidates.html', candidate_data, context_instance=RequestContext(request))

def candidateView(request,candidateName):
	b = New_Candidate.objects.get(name=candidateName)
	data = {
		"detail" : b
	}
	#candidateDetails = getCandidateDetail(candidateName)
	#contextObj = Context({'candidateName':candidateName,'candidateDetails':candidateDetails})
	return render_to_response('test.html',data,context_instance=RequestContext(request))

def register(request):
	return render(request, 'registration_form.html')

def add_candidate(request):
	if request.GET:
		new_candidate = New_Candidate(name=request.GET['name'],post=request.GET['optionsRadios'],  roll=request.GET['roll'], department=request.GET['dept'], cpi=request.GET['cpi'], sem=request.GET['sem'], backlogs=request.GET['back'], email=request.GET['email'], contact=request.GET['contact'], hostel=request.GET['hostel'], room=request.GET['room'], agenda=request.GET['agenda'])
        	new_candidate.save()
	return HttpResponseRedirect('/main')


def discuss(request,o_id):
    '''Discuss Function renders a discussion page for doubts/agendas.It takes input as the request, object id of the agenda
       For GET request it renders the page discuss.html with existing agenda and comments with a form for new Comment.
       For POST Request it checks for the validity of the comment, sets the no. of like to zero and adds to the database.'''
    commentForm = CommentForm()
    c = {}
    c.update(csrf(request))
    agenda = get_object_or_404(Agenda,id=o_id)
    tempUser = Users.objects.filter(id=get_user(request).id)
    show = True                 #show variable is to ensure that only those people who have logged in can see the like button.
    if len(tempUser) == 0:
        show = False
    if request.method=='POST':
        commentForm =CommentForm(request.POST)
        if commentForm.is_valid():
            tempComment = Comments()
            tempComment.content = commentForm.cleaned_data['content']
            try:
                tempComment.author = Users.objects.get(id=get_user(request).id)
            except:
                print "User not found."
            tempComment.likes = 0
            tempComment.save()
            agenda.comments.add(tempComment)
    Anonymous = "Anonymous"
    comments = agenda.comments.all()
    c.update({'agenda':agenda,'comments':comments,'commentForm':commentForm,'Anonymous':Anonymous,'show':show})
    return render(request,'discuss.html',c)

#ab1a507dd0eee136e381

@login_required
def addLikes(request,c_id):
    '''AddLikes takes input as the request and comment id (c_id) in it's parameters, it then checks whether the user has previously liked
       the comment ,if not it adds the like and also store the user-comment_like relationship in the database.
       For future use functionality can be added to show who all has liked the comment.'''
    try:
        comment = Comments.objects.get(id=c_id)
        agenda = Agenda.objects.filter(comments=comment)[0]
        currentUser = Users.objects.filter(id=get_user(request).id)[0]
        if len(CommentLikes.objects.filter(comment=comment,user=currentUser)) == 0:
            obj = CommentLikes()
            obj.comment,obj.user = comment,currentUser
            a = comment.likes
            comment.likes = comment.likes + 1
            b = comment.likes
            comment.save()
            obj.save()
        return HttpResponseRedirect(reverse('discuss',kwargs={'o_id':agenda.id}))
    except Comments.DoesNotExist:
        raise  Http404
    return render(request,'test.html')