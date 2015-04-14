import sys
import re
import json
import copy

from django.shortcuts import render_to_response, render ,get_list_or_404, get_object_or_404
from mainSite.models import *
from django.http import HttpResponse
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from .databaseManager import getCandidateDetail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user

from mainSite.models import Agenda,Comments,CommentLikes
from mainSite.forms import CommentForm

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/gems')

def user_login(request):                      #url for login page is home/login
    if request.method == 'POST':
    	username= request.POST.get('username')
    	password = request.POST.get('password')
    	user = authenticate(username=username,password=password)
    	if user:
    	    if (user.is_active and user.is_staff):
    	        login(request, user)
    	        if len(Users.objects.filter(username=username)) == 0:
    	        	return HttpResponseRedirect('/gems/adminHome')
    	        else:
    	        	return HttpResponseRedirect('/gems/voterHome')
    	    else:
                login(request, user)
                return HttpResponseRedirect('/gems/voterHome')
    	else:
    	    return HttpResponse("your account is diabled")		
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html', {})

@login_required
def voterHome(request):
	return render(request, 'main_page.html')

@login_required
def register(request):
	if len(Users.objects.filter(username=request.user.username)) == 0:
		return HttpResponse("Only people who can vote are eligible for candidature.")
	if len(Candidates.objects.filter(username=request.user.username)) != 0:
		return HttpResponse("You have already registered. 	You can register only once.")
	if request.method == "GET":
		post_i = Posts.objects.all()
		post_data = {
			"post_detail" : post_i
		}
		return render_to_response('registration_form.html', post_data, context_instance=RequestContext(request))
	elif request.method == "POST":
		postname=request.POST['optionsRadios']
		return HttpResponseRedirect('/gems/register/form?postname='+postname)

@login_required
def registrationform(request):
	if(request.method=='GET') :
		if len(Users.objects.filter(username=request.user.username)) == 0:
			return HttpResponse("Only people who can vote are eligible for candidature.")
		postname = request.GET.get('postname')
		x=Posts.objects.get(postname=postname).info_fields
		formFormat = eval(x)
		#FEATURE REQUIREMENT - data is not persistent - venkat
		return render(request, 'form.html', {"formFormat": formFormat ,  "postname":postname })
	
	elif(request.method=='POST') :
		#BUG REPORT - If a candidate submits a form twice, two separate entries are created
		postname = request.POST.dict()["postname"]
		record = copy.deepcopy(request.POST.dict())
		record.pop('csrfmiddlewaretoken')

		files = request.FILES.dict()
		assert(len(Posts.objects.filter(postname=postname)) == 1)
		post = eval(Posts.objects.filter(postname=postname)[0].info_fields)
		photo = None
		for doc in files:
			if doc == 'photo':
				photo = files[doc]
				continue
			field = None
			for candidate_field in post:
				if candidate_field['id'] == doc:
					field = candidate_field
					break
			assert(field != None)
			print field
			reMatch = re.compile(field['validation']+'$')
			if not reMatch.match(files[doc]._name):
				postname = request.GET.get('postname')
				x=Posts.objects.filter(postname=postname)[0].info_fields
				formFormat = eval(x)
				#FEATURE REQUIREMENT - data is not persistent. This can be solved using the back button - venkat
				return render(request, 'form.html', {"formFormat": formFormat ,  "postname":postname, "alert": "Please give the correct file format"}, context_instance=RequestContext(request))

			newDoc = UploadedDocuments(document=files[doc])
			newDoc.save()
			record[doc] = str(newDoc.id)

		assert(photo != None)
		photo_name = files['photo']._name
		if len(photo_name.split('.')) == 0 or photo_name.split('.')[-1] not in ['jpg', 'jpeg', 'png', 'bmp']:
			postname = request.GET.get('postname')
			x=Posts.objects.filter(postname=postname)[0].info_fields
			formFormat = eval(x)
			#FEATURE REQUIREMENT - data is not persistent - venkat
			return render(request, 'form.html', {"formFormat": formFormat ,  "postname":postname, "alert": "Please give the photo in a proper format (jpg, jpeg, png or bmp)"}, context_instance=RequestContext(request))

		reg_cand = Candidates(username=request.user.username,details=json.dumps(record),postname=postname,photo=photo,approved=False)
		reg_cand.save()
		return HttpResponseRedirect('/gems/voterHome')

@login_required
def adminHome(request):
	if len(Users.objects.filter(username=request.user.username)) != 0:
		return HttpResponse('Only administrators are allwoed to access this page!')
	return render(request, 'adminHome.html')

@login_required
def create_form(request):
	if len(Users.objects.filter(username=request.user.username)) != 0:
		return HttpResponse('Only administrators are allwoed to access this page!')
	post_i = Posts.objects.all()
	post_data = {
		"post_detail" : post_i
	}
	return render_to_response('create-form.html', post_data, context_instance=RequestContext(request))

@login_required
def add_form_details(request):
	if len(Users.objects.filter(username=request.user.username)) != 0:
		return HttpResponse('Only administrators are allwoed to access this page!')
	global post1
	global message
	global uid
	post1 = request.GET['optionsRadios']
	message = ''
	uid = 0
	post_i = Posts.objects.get(postname=post1)
	Post_data = {
		"Post_list" : eval(post_i.info_fields)
	}
	return render_to_response('add-form-details.html', Post_data, context_instance=RequestContext(request))

@login_required
def add_fields(request):
	if len(Users.objects.filter(username=request.user.username)) != 0:
		return HttpResponse('Only administrators are allwoed to access this page!')
	flag = 0
	if request.method == "POST":
		formFields = request.POST.dict()
		res = []
		for i in range(100):
			if "label" + str(i) in formFields:
				x = "label" + str(i)
				y = request.POST['fieldType'+str(i)]
				z = request.POST['placeholder'+str(i)]
				options = request.POST['radioOptions'+str(i)]
				validation = request.POST['validation'+str(i)]
				try:
					re.compile(validation)
					is_valid = True
					f = {"description": formFields[x], "id": "field"+str(len(res)), "type": y, "placeholder": z, "options": options, "validation": validation}
				except re.error:
					is_valid = False
					flag = 1
					field = "field"+str(len(res))
					f = {"description": formFields[x], "id": "field"+str(len(res)), "type": y, "placeholder": z, "options": options, "validation": ''}
				res += [f]
		Posts.objects.filter(postname=post1).update(info_fields=res)
	if flag==0:
		return HttpResponseRedirect('/gems/adminHome/create-form/')
	else:
		post_i = Posts.objects.get(postname=post1)
		Post_data = {
			"Post_list" : eval(post_i.info_fields),
			"alert" : "Not a valid regex in " + field
		}
		return render(request, 'add-form-details.html', Post_data, context_instance=RequestContext(request))

@login_required
def add_post(request):
	if len(Users.objects.filter(username=request.user.username)) != 0:
		return HttpResponse('Only administrators are allwoed to access this page!')
	if request.method == "GET":
		new_post = Posts(postname=request.GET['post_name'],info_fields='[]')
		new_post.save()
	return HttpResponseRedirect('/gems/adminHome/create-form')

@login_required
def view_candidate_information(request):
	if request.method == "POST":
		candidate_username = request.POST['username']
		candidate = Candidates.objects.filter(username=candidate_username)
		if len(candidate) == 0:# or candidate[0].approved == False:
			return HttpResponse("Sorry, no such candidate exists")
		assert(len(candidate) == 1)
		candidate = candidate[0]
		if len(Users.objects.filter(username=request.user.username)) != 0:
			sys.stderr.write("Hack Attempt: User: "+request.users.username+" tried to approve/disapprove candidates.")
			return HttpResponse("Only admins are allowed to approve/disapprove candidates. This will be reported!!") #this is why we require login
		candidate.approved = not candidate.approved
		candidate.save()
		return HttpResponseRedirect('/gems/candidates/view-candidate-list')
		
	candidate_username = request.GET['user']
	candidate = Candidates.objects.filter(username=candidate_username)
	if len(candidate) == 0:# or candidate[0].approved == False:
		return HttpResponse("Sorry, no such candidate exists")
	assert(len(candidate) == 1)
	candidate = candidate[0]

	candidate_name = Users.objects.filter(username=candidate_username)[0].name
	candidate_photo = "/media/" + candidate.photo.name

	details = candidate.details
	details = json.loads(details)
	post = Posts.objects.filter(postname=candidate.postname)
	assert(len(post) == 1)
	post = post[0]

	fields = eval(post.info_fields)
	detailsList = []
	for x in details:
		if x == 'postname' or x == 'agree':
			continue
		field = None
		for f in fields:
			#print details[x]
			if f['id'] == x:
				field = f
				break

		assert(field != None)
		if field['type'] == 'file':
			value = "/media/" + UploadedDocuments.objects.filter(id=details[x])[0].document.name
		else:
			value = details[x]
		detailsList += [{'description': field['description'], 'value': value, 'type': field['type']}]

	#reverse the list
	detailsList1 = []
	for x in range(len(detailsList)-1, -1, -1):
		detailsList1 += [detailsList[x]]

	isAdmin, isApproved = False, None
	if len(Users.objects.filter(username=request.user.username)) == 0: #ie. admin. So display option to approve/disapprove candidates
		isAdmin = True
		isApproved = candidate.approved

	if not isApproved and not isAdmin:
		return HttpResponse("Sorry, no such candidate exists") #deliberately chose the same string so that information is not leaked

	return render(request, 'view-candidate-information.html', {'details': detailsList1, 'photo': candidate_photo, 'username': candidate_username, 'candidateName': candidate_name, 'isAdmin': isAdmin, 'isApproved': isApproved})

def view_candidate_list(request):
	if not request.method == "GET":
		raise IOError
	candidates = Candidates.objects.all()
	res = {}
	for candidate in candidates:
		try:
			name = Users.objects.filter(username=candidate.username)[0].name
		except IndexError:
			continue #For debugging purposes only
			assert(False)
		if not candidate.postname in res:
			res[candidate.postname] = []
		res[candidate.postname] += [{'username': candidate.username, 'name': name}]
	return render(request, 'view-candidate-list.html', {'posts': res})

def discuss(request,o_id):
    '''Discuss Function renders a discussion page for doubts/agendas.It takes input as the request, object id of the agenda
       For GET request it renders the page discuss.html with existing agenda and comments with a form for new Comment.
       For POST Request it checks for the validity of the comment, sets the no. of like to zero and adds to the database.'''
    commentForm = CommentForm()
    c = {}
    c.update(csrf(request))
    agenda = get_object_or_404(Agenda,id=o_id)
    tempUser = Users.objects.filter(id=get_user(request).id)
    
    candidateName = agenda.candidate.name
    candidateObj = Candidates.objects.filter(username=agenda.candidate.username)[0]
    candidatePost = candidateObj.postname

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
    c.update({'agenda':agenda,'comments':comments,'commentForm':commentForm,'Anonymous':Anonymous,'show':show, 'candidateName': candidateName, 'candidatePost': candidatePost, 'candidateUsername': agenda.candidate.username})
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