from django.shortcuts import render_to_response, render
from mainSite.models import *
import json
from django.http import HttpResponse
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from .databaseManager import getCandidateDetail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import re

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
	return render_to_response('test.html',data,context_instance=RequestContext(request))

def register(request):
	return render(request, 'registration_form.html')

def adminHome(request):
	return render(request, 'adminHome.html')

def create_form(request):
	post_i = Posts.objects.all()
	post_data = {
		"post_detail" : post_i
	}
	return render_to_response('create-form.html', post_data, context_instance=RequestContext(request))

def add_form_details(request):
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

def add_fields(request):
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
				except re.error:
					is_valid = False
					post_i = Posts.objects.get(postname=post1)
					Post_data = {
						"Post_list" : eval(post_i.info_fields),
						"alert" : "Not a valid regex"
					}
					return render(request, 'add-form-details.html', Post_data, context_instance=RequestContext(request))
				f = {"description": formFields[x], "id": "field"+str(len(res)), "type": y, "placeholder": z, "options": options, "validation": validation}
				res += [f]
		Posts.objects.filter(postname=post1).update(info_fields=res)
	return HttpResponseRedirect('/gems/adminHome/create-form')

def add_post(request):
	if request.method == "GET":
		new_post = Posts(postname=request.GET['post_name'],info_fields='')
		new_post.save()
	return HttpResponseRedirect('/gems/adminHome/create-form')

def view_candidate_information(request):
	if not request.method == "GET":
		raise IOError

	candidate_username = request.GET['user']
	candidate = Candidates.objects.filter(username=candidate_username)
	if len(candidate) == 0 or candidate[0].approved == False:
		return HttpResponse("Sorry, no such candidate exists")
	assert(len(candidate) == 1)
	candidate = candidate[0]

	candidate_photo = candidate.photo

	details = candidate.details
	details = json.loads(details)
	post = Posts.objects.filter(postname=candidate.postname)
	assert(len(post) == 1)
	post = post[0]

	fields = eval(post.info_fields)
	for x in details:
		field = None
		for f in fields:
			if f['id'] == x['id']:
				field = f
				break
		assert(field != None)
		x['description'] = field['description']

	return render(request, 'view-candidate-information.html', {'details': details, 'photo': candidate_photo, 'username': candidate_username})
