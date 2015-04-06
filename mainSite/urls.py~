from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from mainSite.models import Candidates
from mainSite import views

urlpatterns = patterns('',
	url(r'^register', views.register),
	url(r'^view$', views.view_candidate),
	url(r'^$', views.logged),
	url(r'^view/(?P<candidateName>[-\w]+)/$',views.candidateView , name = 'candidatePage'),
	#url(r'^search-form/$', views.search_form),
	(r'^search/$', views.search),
)
