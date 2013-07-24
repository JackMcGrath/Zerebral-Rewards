from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # enable admin
    url(r'^admin/', include(admin.site.urls)),

    # auth endpoints
    url(r'^login/$', 'auth.views.login'),
	url(r'^register/$', 'auth.views.register'),
	(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

	# apps for each 
    url(r'^teacher/', include('teachers.urls')),
    url(r'^student/', include('students.urls')),
    url(r'^parent/', include('parents.urls')),
    url(r'^school/', include('schools.urls')),

    # catch all (we'll forward them to login page)
    url(r'^$', 'auth.views.login'),
)