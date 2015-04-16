from django.test import TestCase,Client
from mainSite.models import Posts, Votes
from mainSite import views
from mainSite import databaseManager
from django.contrib.auth.models import UserManager,User

class ClientTest(TestCase):
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

	def test_success_login(self):
		# Issue a GET request.
		response = self.client.post('/gems/login',{ 'username' : 'kayush', 'password' : self.passy[0] })
		self.assertEqual(response.status_code, 302)
		self.assertNotEqual(response.content, 'your account is diabled')

	def test_fail_login(self):
		response = self.client.post('/gems/login',{ 'username' : 'kayush', 'password' : self.passy[1] })
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, 'your account is diabled')

	def test_fail_logout(self):
		response = self.client.post('/gems/logout')
		self.assertEqual(response.content,'')

	# def test_success_logout(self):
	# 	user = self.client.login(username = 'kayush', password = self.passy[0])
	# 	self.assertTrue(user)
	# 	response = self.client.post('/gems/logout',follow=True)
	# 	self.assertRedirects(response,'/gems')

	def test_admin_add_post(self):
		self.assertTrue(self.superusers)
		user = self.client.login(username = 'kunal', password = 'kunal')
		self.assertTrue(user)
		response = self.client.get('/gems/adminHome/create-form/add-post', {'post_name' : 'vp'}, follow=True)
		self.assertRedirects(response,'/gems/adminHome/create-form')

	def test_user_add_post(self):
		user = self.client.login(username = 'kayush', password = self.passy[0])
		self.assertTrue(user)
		response = self.client.get('/gems/adminHome/create-form/add-post', {'post_name' : 'vp'}, follow=True)
		self.assertEqual(response.content, 'Only administrators are allwoed to access this page!')

	def test_admin_duplicate_post(self):
		self.assertTrue(self.superusers)
		user = self.client.login(username = 'kunal', password = 'kunal')
		self.assertTrue(user)
		response = self.client.get('/gems/adminHome/create-form/add-post', {'post_name' : 'vp'}, follow=True)
		self.assertRedirects(response,'/gems/adminHome/create-form')
		response1 = self.client.get('/gems/adminHome/create-form/add-post', {'post_name' : 'vp'}, follow=True)
		self.assertEqual(response1.content, 'Duplicate Post')
