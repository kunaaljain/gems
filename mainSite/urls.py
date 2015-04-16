from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from mainSite.models import Candidates
from mainSite import views

urlpatterns = patterns('',
	url(r'^logout$', views.user_logout),
	url(r'^register/$', views.register),
	url(r'^register/form', views.registrationform),
	url(r'^voterHome$', views.voterHome),
	url(r'^voterHome/voting-page$',views.voterView),
	url(r'^voterHome/voter-info$', views.voter_info),
	url(r'^login$', views.user_login, name='login'),
	url(r'^adminHome$', views.adminHome, name='adminHome'),
	url(r'^adminHome/create-form$', views.create_form),
	url(r'^adminHome/create-form/add-form-details$', views.add_form_details),
	url(r'^adminHome/create-form/add-fields$', views.add_fields),
	url(r'^adminHome/election-state$',views.change_electionstate),
	url(r'^adminHome/create-form/add-post$', views.add_post),
	url(r'^adminHome/register-users$', views.register_users),
	url(r'^candidates/view-candidate-information$', views.view_candidate_information),
	url(r'^candidates/view-candidate-list$', views.view_candidate_list),
	url(r'^discuss/(?P<o_id>\d+)/$', views.discuss,name='discuss'),
	url(r'^discuss/list/$', views.discuss_list,name='discuss'),
	url(r'^addLikes/(?P<c_id>\d+)/$',views.addLikes,name='addLikes'),
	url(r'^results/results-page$', views.results_page), 
	url(r'^results/selected-list$', views.selectedCandidates)
 )
