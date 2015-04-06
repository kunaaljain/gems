from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from mainSite.models import Candidates
from mainSite import views
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^register', views.register),
	url(r'^view$', views.view_candidate),
	url(r'^voterHome$', views.voterHome),
	url(r'^view/(?P<candidateName>[-\w]+)/$',views.candidateView , name = 'candidatePage'),
	url(r'^add_candidate$', views.add_candidate),
    url(r'^login$', views.user_login, name='login')
    , url(r'^results/$',views.resultsView , name = 'results')
	, url(r'^candidates/$',views.candidatesListView , name = 'candidates')
	, url(r'^candidates/(?P<candidateName>[-\w]+)/$',views.candidateView , name = 'candidatePage')
	, url(r'^results/(?P<candidateName>[-\w]+)/$',views.candidateStat)
	,
 )

