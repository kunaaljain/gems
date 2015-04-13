from django.db import models
from django.forms import ModelForm

# Create your models here.
class Users(models.Model):
	username = models.CharField(max_length=50, unique=True)
	voted = models.BooleanField()
	department = models.CharField(max_length=100)
	name = models.CharField(max_length=50)
	course = models.CharField(max_length=30)
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
	postname = models.CharField(max_length=50)
	info_fields = models.CharField(max_length=10000)
	def __unicode__(self):
		return self.postname

class UploadedDocuments(models.Model):
	document = models.FileField(upload_to='documents/other_uploads/%Y/%m/%d')