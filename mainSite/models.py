from django.db import models
from django.forms import ModelForm

# Create your models here.
class Users(models.Model):
	username = models.CharField(max_length=50, unique=True)
	voted = models.BooleanField()
	department = models.CharField(max_length=100)
	name = models.CharField(max_length=50)
	course = models.CharField(max_length=30)
	gender = models.CharField(max_length=1) #either 'm' or 'f'
	hostel = models.CharField(max_length=30)
	encryptedPrivateKey = models.CharField(max_length=4096)
	'''Non empty only when user is logged in'''
	plaintextPrivatekey = models.CharField(max_length=2048)

	def __unicode__(self):
        	return self.name

#Create database for storing posts

class Candidates(models.Model):
	username = models.CharField(max_length=50)
	details = models.CharField(max_length=10000)
	postname = models.CharField(max_length=50)
	photo = models.FileField(upload_to='documents/candidate_photos/%Y/%m/%d')
	approved = models.BooleanField()
	voteInfo = models.CharField(max_length=500)
	def __unicode__(self):
        	return self.username

class Votes(models.Model):
	plainText = models.CharField(max_length=50)
	certificate = models.CharField(max_length=60)

	publicKey = models.ForeignKey("PublicKeys")
	challengeStr = models.ForeignKey("ChallengeStrings")

class ChallengeStrings(models.Model):
	challengeStr = models.CharField(max_length=2048)

class PublicKeys(models.Model):
	publicKey = models.CharField(max_length=2048)

class Posts(models.Model):
	eligibleGender = models.CharField(max_length=1) #either 'm' or 'f'
	eligibleCourse = models.CharField(max_length=5) #either 'btech', 'mtech', 'phd', 'other', 'prof' or 'a'
	postCount = models.IntegerField()
	postname = models.CharField(max_length=50)
	info_fields = models.CharField(max_length=10000)
	def __unicode__(self):
		return self.postname

class UploadedDocuments(models.Model):
	document = models.FileField(upload_to='documents/other_uploads/%Y/%m/%d')

class Comments(models.Model):
	author = models.ForeignKey(Users,null=True)
	content = models.CharField(max_length=80000)
	likes = models.BigIntegerField()
	def __unicode__(self):
		return self.content

class Agenda(models.Model):
	candidate = models.ForeignKey(Users)
	content = models.CharField(max_length=80000)
	comments = models.ManyToManyField("Comments",blank=True)

class CommentLikes(models.Model):
	user = models.ForeignKey(Users)
	comment = models.ForeignKey(Comments)

class GlobalVariables(models.Model):
	'''To store miscellaneous global variables such as election state.'''
	varname = models.CharField(max_length=128, unique=True)
	value = models.CharField(max_length=128)