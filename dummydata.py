# to run this file from cmmand line you will have to enter the following cammand
# python manage.py shell < dummydata.py

from mainSite.databaseManager import addUser, addCandidate, addVotes, addChallengeStrings, addPublicKeys
addUser('kayush', False, 'cse' , 'Ayush', 'btech','qweqwrqwr');
addUser('adgfd', False, 'cse' , 'sdg', 'btech','sdghdf');
addUser('Student1', False, 'cse' , 'Nice Name', 'mtech','password');
addUser('Student2', False, 'cse' , 'Hiyaa', 'btech','hello world');
addCandidate('Student1', 'resides in umium hostel at room no a3-56', '/static/sudhanshu.jpg', False);
addCandidate('adgfd', 'resides in umium hostel at room no a3-56', '/static/sudhanshu.jpg', False);
#addVotes('["yes",]')
