# to run this file from cmmand line you will have to enter the following cammand
# python manage.py shell < dummydata.py

from mainSite.databaseManager import addUser, addCandidate, addVotes, addChallengeStrings, addPublicKeys
addUser('kayush', False, 'cse' , 'Ayush', 'btech','qweqwrqwr');
addCandidate('sudhanshu2013', 'resides in umium hostel at room no a3-56', '/static/sudhanshu.jpg',' ');
#addVotes('["yes",]')
