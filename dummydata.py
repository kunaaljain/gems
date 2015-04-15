import os
from mainSite import databaseManager
from django.core.management import call_command

# call_command('makemigrations', interactive = False)
# call_command('migrate', interactive = False)

#call_command('syncdb', interactive = True)
 
#This part is essential to the functioning of the system:
from mainSite.models import *
GlobalVariables(varname='electionState', value='pre-election').save()

 #This is optional

userList = [{'username':'kayush', 'department':'cs', 'name':'Ayush', 'course':'btech', 'hostel' : 'siang', 'gender': 'm'},
		 {'username':'adgfd', 'department':'cs', 'name':'sdg', 'course':'btech', 'hostel' : 'kameng', 'gender': 'm'},
		 {'username':'Student1', 'department':'ee', 'name':'Nice Name', 'course':'mtech', 'hostel' : 'subuansiri', 'gender': 'f'},
		 {'username':'Student2', 'department':'dd', 'name':'Hiyaa', 'course':'phd', 'hostel' : 'siang', 'gender': 'm'}
		]

passy = databaseManager.registerUsers(userList)

# databaseManager.makeCandidate('adgfd','[{"id": "field0", "type": "text", "value": "Ad Fg Jkl"}, {"id": "field1", "type": "radio", "value": "Male"}, {"id": "field2", "type": "file", "value": "/agendas/not-available.pdf"}]', 'Vice President', '/static/candidates/photos/adgfd.jpg', True)

from mainSite.models import Posts
post = Posts(postname="Vice President", postCount=1, eligibleGender='a', eligibleCourse='a', info_fields="[{'description': u'Name', 'type': u'text', 'id': 'field0', 'validation': u'', 'placeholder': u'', 'options': u''}, {'description': u'Gender', 'type': u'radio', 'id': 'field1', 'validation': u'', 'placeholder': u'', 'options': u'Male; Female'}, {'description': u'Agenda', 'type': u'file', 'id': 'field2', 'validation': u'.*\.pdf', 'placeholder': u'', 'options': u''}]")
post.save()

print passy
#databaseManager.registerVote("some text pertaining to a vote", "kayush", passy[0])
#databaseManager.registerVote("some text pertaining to a vote", "kayush", passy[0])
#databaseManager.registerVote("some text pertaining to a vote", "kayush", passy[0])

#sampe post info_fields
#[{'description': u'Name', 'type': u'text', 'id': 'field0', 'validation': u'', 'placeholder': u'Your Name', 'options': u''}, {'description': u'Date of Birth', 'type': u'text', 'id': 'field1', 'validation': u'[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]', 'placeholder': u'DOB - dd-mm-yyyy', 'options': u''}, {'description': u'Agenda', 'type': u'file', 'id': 'field2', 'validation': u'.*.pdf', 'placeholder': u'', 'options': u''}]

#['d729aa3485637e8d384d', '5b36e6efa123f7003717', 'cd7ba755452a311d311c']
