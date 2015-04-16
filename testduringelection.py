from django.test import TestCase
from mainSite.models import Posts, Votes, GlobalVariables
from mainSite import views
from mainSite import databaseManager

class  duringelection(TestCase):
	def __init__(self, *args, **kwargs):
		super(duringelection, self).__init__(*args, **kwargs)
		self.passy = []

	def setUp(self):
		Posts.objects.create(postname="Vice President", postCount=1, eligibleGender='a', eligibleCourse='a', info_fields="[{'description': u'Name', 'type': u'text', 'id': 'field0', 'validation': u'', 'placeholder': u'', 'options': u''}, {'description': u'Gender', 'type': u'radio', 'id': 'field1', 'validation': u'', 'placeholder': u'', 'options': u'Male; Female'}, {'description': u'Agenda', 'type': u'file', 'id': 'field2', 'validation': u'.*\.pdf', 'placeholder': u'', 'options': u''}]")
		userList = [{'username':'kayush', 'department':'cs', 'name':'Ayush', 'course':'btech', 'hostel' : 'siang', 'gender': 'm'},
		 {'username':'adgfd', 'department':'cs', 'name':'sdg', 'course':'btech', 'hostel' : 'kameng', 'gender': 'm'},
		 {'username':'Student1', 'department':'ee', 'name':'Nice Name', 'course':'mtech', 'hostel' : 'subuansiri', 'gender': 'f'},
		 {'username':'Student2', 'department':'dd', 'name':'Hiyaa', 'course':'phd', 'hostel' : 'siang', 'gender': 'm'}
		]
		self.passy = databaseManager.registerUsers(userList)
		GlobalVariables(varname='electionState', value='election').save()

	def test_post_present(self):
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
		self.assertTrue(databaseManager.registerVote("some text pertaining to a vote1", "kayush", self.passy[0]))
		self.assertTrue(databaseManager.registerVote("some text pertaining to a vote2", "kayush", self.passy[0]))
		self.assertEqual(len(Votes.objects.all()),3)
		val = databaseManager.verifyVote()
		self.assertTrue(val)
