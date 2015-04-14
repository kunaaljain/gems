# to run this file from cmmand line you will have to enter the following cammand
# python manage.py shell < dummydata.py

import os
from mainSite import databaseManager
from django.core.management import call_command

os.remove('db.sqlite3')
call_command('syncdb', interactive = False)

userList = [{'username':'kayush', 'department':'cse', 'name':'Ayush', 'course':'btech', 'hostel' : 'Siang'},
		 {'username':'adgfd', 'department':'cse', 'name':'sdg', 'course':'btech', 'hostel' : 'Kameng'},
		 {'username':'Student1', 'department':'ece', 'name':'Nice Name', 'course':'mtech', 'hostel' : 'Subuansiri'},
		 {'username':'Student2', 'department':'des', 'name':'Hiyaa', 'course':'phd', 'hostel' : 'Siang'}
		]
databaseManager.makeCandidate('adgfd','some details','a')

passy = databaseManager.registerUsers(userList)
print passy
databaseManager.registerVote("some text pertaining to a vote", "kayush", passy[0])
databaseManager.registerVote("some text pertaining to a vote", "kayush", passy[0])
databaseManager.registerVote("some text pertaining to a vote", "kayush", passy[0])
