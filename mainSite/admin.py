from django.contrib import admin
from mainSite.models import *

# Register your models here.


from mainSite.models import User, Candidates,Votes, PublicKeys, ChallengeStrings ,Posts
admin.site.register(User)
admin.site.register(Candidates)
admin.site.register(Votes)
admin.site.register(PublicKeys)
admin.site.register(ChallengeStrings)
admin.site.register(Posts)
