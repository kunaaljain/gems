from django.db import models

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=50)
	voted = models.BooleanField()
	department = models.CharField(max_length=100)
	name = models.CharField(max_length=50)
	course = models.CharField(max_length=30)
	encryptedPrivateKey = models.CharField(max_length=2048)
	
	def __unicode__(self):
        	return self.name


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

class ChallengeStrings(models.Model):
	challengeStr = models.CharField(max_length = 2048)

class PublicKeys(models.Model):
	publicKey = models.CharField(max_length=2048)

# more fields to be added 

class Posts(models.Model):
	postName = models.CharField(max_length=50)
	postCount = models.IntegerField(max_length=3)
	voterGender = models.CharField(max_length=1)    #'M'/'F'/'any'
	voterCourse = models.CharField(max_length=2)		# 'UG'/'PG'/'any'
	eligibleGender = models.CharField(max_length=1)		#'M'/'F'/'any'
	eligibleCourse = models.CharField(max_length=2)     #'UG'/"PG"/'any'
	eligibleYear = models.CharField(max_length=2)		#minimum requirement of year

