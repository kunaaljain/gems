from django.test import TestCase,Client
from mainSite.models import Posts, Votes
from mainSite import views
from mainSite import databaseManager
from django.contrib.auth.models import UserManager,User

class ClientTest1(TestCase):
	def setUp(self):
		# Every test needs a client.
		# f62a6eec3d340b45f857
		self.client = Client()
		userList = [{'username':'kayush', 'department':'cs', 'name':'Ayush', 'course':'btech', 'hostel' : 'siang', 'gender': 'm'},
		 {'username':'adgfd', 'department':'cs', 'name':'sdg', 'course':'btech', 'hostel' : 'kameng', 'gender': 'm'},
		 {'username':'Student1', 'department':'ee', 'name':'Nice Name', 'course':'mtech', 'hostel' : 'subuansiri', 'gender': 'f'},
		 {'username':'Student2', 'department':'dd', 'name':'Hiyaa', 'course':'phd', 'hostel' : 'siang', 'gender': 'm'}
		]
		self.passy = databaseManager.registerUsers(userList)
		self.superusers = User.objects.create_superuser(username = 'kunal',password = 'kunal', email = 'kunaalus@gmail.com')

	def test_fail_login(self):
		response = self.client.post('/gems/voterHome/voting-page',{ 'username' : 'asas', 'password' : self.passy[1] })
		# self.assertEqual(response.status_code, 200)
		# self.assertEqual(response.content, 'your account is diabled')