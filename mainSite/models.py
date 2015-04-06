from django.db import models
from django.forms import ModelForm

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=50)
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
	photo = models.CharField(max_length=100)
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

class CandidateForm(ModelForm):
    class Meta:
        model = Candidates
        #fields = ['username', 'details']

class New_Candidate(models.Model):
	name = models.CharField(max_length=50)
	post = models.CharField(max_length=4 ,default='')
	roll = models.IntegerField(max_length=10, default='')
	department = models.CharField(max_length=100, default='')
	cpi = models.FloatField(max_length=4, default='')
	sem = models.IntegerField(max_length=1, default='')
	backlogs = models.CharField(max_length=50, default='')
	email = models.CharField(max_length=50, default='')
	contact = models.IntegerField(max_length=10, default='')
	hostel = models.CharField(max_length=10,default='')
	room = models.CharField(max_length=10, default='')
	agenda = models.CharField(max_length=100000, default='')
	def __unicode__(self):
        	return self.name
