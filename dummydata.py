import os
from mainSite import databaseManager
from django.core.management import call_command

# call_command('makemigrations', interactive = False)
# call_command('migrate', interactive = False)

call_command('syncdb', interactive = True)
 
#This part is essential to the functioning of the system:
from mainSite.models import *
# GlobalVariables(varname='electionState', value='pre-election').save()

 #This is optional

userList = [{'username':'kayush', 'department':'cs', 'name':'Ayush', 'course':'btech', 'hostel' : 'siang', 'gender': 'm'},
		 {'username':'adgfd', 'department':'cs', 'name':'sdg', 'course':'btech', 'hostel' : 'kameng', 'gender': 'm'},
		 {'username':'Student1', 'department':'ee', 'name':'Nice Name', 'course':'mtech', 'hostel' : 'subuansiri', 'gender': 'f'},
		 {'username':'Student2', 'department':'dd', 'name':'Hiyaa', 'course':'phd', 'hostel' : 'siang', 'gender': 'm'},
		 {'username':'Student3', 'department':'me', 'name':'Very Nice Name', 'course':'phd', 'hostel' : 'siang', 'gender': 'm'},
		 {'username':'Student4', 'department':'dd', 'name':'Name1', 'course':'phd', 'hostel' : 'siang', 'gender': 'm'},
		 {'username':'Student5', 'department':'dd', 'name':'Name2', 'course':'phd', 'hostel' : 'siang', 'gender': 'm'},
		 {'username':'Student6', 'department':'cs', 'name':'Hiyaa', 'course':'phd', 'hostel' : 'siang', 'gender': 'm'},
		 {'username':'Student7', 'department':'cs', 'name':'Hiyaa', 'course':'mtech', 'hostel' : 'kameng', 'gender': 'm'},
		 {'username':'Student8', 'department':'cs', 'name':'Hiyaa', 'course':'mtech', 'hostel' : 'kameng', 'gender': 'm'},
		 {'username':'Student9', 'department':'ee', 'name':'Hiyaa', 'course':'mtech', 'hostel' : 'kameng', 'gender': 'm'},
		 {'username':'Student10', 'department':'ee', 'name':'Hiyaa', 'course':'btech', 'hostel' : 'kapili', 'gender': 'm'},
		 {'username':'Student11', 'department':'ee', 'name':'Hiyaa', 'course':'btech', 'hostel' : 'kapili', 'gender': 'm'},
		 {'username':'Student12', 'department':'me', 'name':'Hiyaa', 'course':'btech', 'hostel' : 'kapili', 'gender': 'm'},
		 {'username':'Student13', 'department':'me', 'name':'Hiyaa', 'course':'btech', 'hostel' : 'subhansiri', 'gender': 'f'},
		 {'username':'Student14', 'department':'dd', 'name':'Hiyaa', 'course':'btech', 'hostel' : 'subhansiri', 'gender': 'f'},
		 {'username':'Student15', 'department':'dd', 'name':'Hiyaa', 'course':'mtech', 'hostel' : 'subhansiri', 'gender': 'f'}]

passy = databaseManager.registerUsers(userList)

# databaseManager.makeCandidate('adgfd','[{"id": "field0", "type": "text", "value": "Ad Fg Jkl"}, {"id": "field1", "type": "radio", "value": "Male"}, {"id": "field2", "type": "file", "value": "/agendas/not-available.pdf"}]', 'Vice President', '/static/candidates/photos/adgfd.jpg', True)

from mainSite.models import Posts

print passy

#Add some posts
post1=Posts(postname='Vice President', info_fields=[{'description': u'Agenda', 'type': u'file', 'id': 'field0', 'validation': u'.*\\.pdf', 'placeholder': u'', 'options': u''}], eligibleGender='a', eligibleCourse='a', postCount = 1)
post1.save()

post2=Posts(postname='Senators (UG)', info_fields=[{'description': u'Agenda', 'type': u'file', 'id': 'field0', 'validation': u'.*\\.pdf', 'placeholder': u'', 'options': u''}, {'description': u'Course', 'type': u'radio', 'id': 'field1', 'validation': u'UG', 'placeholder': u'', 'options': u'UG; PG; Other'}], eligibleGender='a', eligibleCourse='btech', postCount = 3)
post2.save()

post3=Posts(postname='Senators (Girls)', info_fields=[{'description': u'Agenda', 'type': u'file', 'id': 'field0', 'validation': u'.*\\.pdf', 'placeholder': u'', 'options': u''}, {'description': u'Gender', 'type': u'radio', 'id': 'field', 'validation': u'Female', 'placeholder': u'', 'options': u'Female; Male'}], eligibleGender='f', eligibleCourse='a', postCount = 1)
post3.save()

GlobalVariables(varname='electionState', value='election').save()
databaseManager.registerVote("some text pertaining to a vote", "kayush", passy[0])
databaseManager.registerVote("some text pertaining to a vote1", "kayush", passy[0])
databaseManager.registerVote("some text pertaining to a vote2", "kayush", passy[0])
databaseManager.verifyVote()
#sampe post info_fields
#[{'description': u'Name', 'type': u'text', 'id': 'field0', 'validation': u'', 'placeholder': u'Your Name', 'options': u''}, {'description': u'Date of Birth', 'type': u'text', 'id': 'field1', 'validation': u'[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]', 'placeholder': u'DOB - dd-mm-yyyy', 'options': u''}, {'description': u'Agenda', 'type': u'file', 'id': 'field2', 'validation': u'.*.pdf', 'placeholder': u'', 'options': u''}]

#['d729aa3485637e8d384d', '5b36e6efa123f7003717', 'cd7ba755452a311d311c']
