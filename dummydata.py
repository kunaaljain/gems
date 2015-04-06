# to run this file from cmmand line you will have to enter the following cammand
# python manage.py shell < dummydata.py

from mainSite import databaseManager
'''addUser('kayush', False, 'cse' , 'Ayush', 'btech','qweqwrqwr');
from mainSite.databaseManager import addUser, addCandidate, addVotes, addChallengeStrings, addPublicKeys

addUser('kayush', False, 'cse' , 'Ayush', 'btech','qweqwrqwr');
>>>>>>> ef0c76940b176eb69b618a88f972a950471b88fb
addUser('adgfd', False, 'cse' , 'sdg', 'btech','sdghdf');
addUser('Student1', False, 'cse' , 'Nice Name', 'mtech','password');
addUser('Student2', False, 'cse' , 'Hiyaa', 'btech','hello world');
addCandidate('Student1', 'resides in umium hostel at room no a3-56', '/static/sudhanshu.jpg', False);
addCandidate('adgfd', 'resides in umium hostel at room no a3-56', '/static/sudhanshu.jpg', False);
#addVotes('["yes",]')'''

userList = [{'username':'kayush', 'department':'cse', 'name':'Ayush', 'course':'btech'},
		 {'username':'adgfd', 'department':'cse', 'name':'sdg', 'course':'btech'},
		 {'username':'Student1', 'department':'ece', 'name':'Nice Name', 'course':'mtech'},
		 {'username':'Student2', 'department':'des', 'name':'Hiyaa', 'course':'phd'}
		]

passy = databaseManager.registerUsers(userList)
print passy
databaseManager.registerVote("some text pertaining to a vote", "kayush", passy[0])
databaseManager.registerVote("some text pertaining to a vote", "kayush", passy[0])
databaseManager.registerVote("some text pertaining to a vote", "kayush", passy[0])
