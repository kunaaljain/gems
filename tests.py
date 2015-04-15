from django.test import TestCase
from mainSite.models import Posts, Votes
from mainSite import views
from mainSite import databaseManager

class  dbtest(TestCase):
	def __init__(self, *args, **kwargs):
		super(dbtest, self).__init__(*args, **kwargs)
		self.passy = []

	def setUp(self):
		Posts.objects.create(postname="Vice President", info_fields="[{'description': u'Name', 'type': u'text', 'id': 'field0', 'validation': u'', 'placeholder': u'', 'options': u''}, {'description': u'Gender', 'type': u'radio', 'id': 'field1', 'validation': u'', 'placeholder': u'', 'options': u'Male; Female'}, {'description': u'Agenda', 'type': u'file', 'id': 'field2', 'validation': u'.*\.pdf', 'placeholder': u'', 'options': u''}]")
		userList = [{'username':'kayush', 'department':'cse', 'name':'Ayush', 'course':'btech', 'hostel' : 'Siang'},
		 {'username':'adgfd', 'department':'cse', 'name':'sdg', 'course':'btech', 'hostel' : 'Kameng'},
		 {'username':'Student1', 'department':'ece', 'name':'Nice Name', 'course':'mtech', 'hostel' : 'Subuansiri'},
		 {'username':'Student2', 'department':'des', 'name':'Hiyaa', 'course':'phd', 'hostel' : 'Siang'}
		]
		self.passy = databaseManager.registerUsers(userList)

	def test_animals_can_speak(self):
		"""Animals that can speak are correctly identified"""
		vp = Posts.objects.get(postname="Vice President")
		self.assertEqual(vp.postname,"Vice President")

	def test_votes(self):
		self.assertTrue(databaseManager.registerVote("some text pertaining to a vote", "kayush", self.passy[0]))

	def test_verify_cast_vote(self):
		self.assertTrue(databaseManager.registerVote("some text pertaining to a vote", "kayush", self.passy[0]))
		self.assertEqual(len(Votes.objects.all()),1)

	def test_verify_votes(self):
		self.assertTrue(databaseManager.registerVote("some text pertaining to a vote", "kayush", self.passy[0]))
		self.assertEqual(len(Votes.objects.all()),1)
		val = databaseManager.verifyVote(Votes.objects.all())
		self.assertTrue(val)
