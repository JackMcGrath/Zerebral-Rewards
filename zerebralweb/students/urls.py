from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns('',
	url(r'^dashboard', 'students.views.dashboard'),

	# first view should always be dashboard
	url(r'^$', RedirectView.as_view(url='/student/dashboard')),
)