from django.conf.urls import patterns, include, url
from django.contrib import admin
from mainSite import views


urlpatterns  = patterns('' , url(r'^results/$',views.resultsView , name = 'results')
						   , url(r'^candidates/$',views.candidatesListView , name = 'candidates')
						   , url(r'^candidates/(?P<candidateName>[-\w]+)/$',views.candidateView , name = 'candidatePage')
						   , url(r'^results/(?P<candidateName>[-\w]+)/$',views.candidateStat)
						   ,
						)
