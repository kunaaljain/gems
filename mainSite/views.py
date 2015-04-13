from django.shortcuts import render_to_response, render
from mainSite.models import *
import json, copy
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

def register(request):
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
<<<<<<< HEAD
		postName = request.POST.dict()["postname"]
		post = Posts.objects.filter(postname = postName).info_fields
		record = copy.deepcopy(request.POST.dict())
		record.pop('csrfmiddlewaretoken')
		record.pop('agree')
		res = []
		for Id in record:
			res += [{'id': Id, 'value': record[Id], 'type': 'text'}]
		reg_cand = Candidates(username='b',details=json.dumps(record),postname=postName,photo='',approved=False)
=======
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
>>>>>>> a73e8dbb5ff7b75404bff6d33c19a78def037590
		reg_cand.save()
		return HttpResponseRedirect('/gems/voterHome')

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
		new_post = Posts(postname=request.GET['post_name'],info_fields='[]')
		new_post.save()
	return HttpResponseRedirect('/gems/adminHome/create-form')

def view_candidate_information(request):
	if not request.method == "GET":
		raise IOError
	if not 'user' in request.GET:
		return HttpResponse("You must have come here by mistake. Please mention the candidate.")
	candidate_username = request.GET['user']
	candidate = Candidates.objects.filter(username=candidate_username)
	if len(candidate) == 0:# or candidate[0].approved == False:
		return HttpResponse("Sorry, no such candidate exists")
	assert(len(candidate) == 1)
	candidate = candidate[0]

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

	return render(request, 'view-candidate-information.html', {'details': detailsList1, 'photo': candidate_photo, 'username': candidate_username})

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
