from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # enable admin
    url(r'^admin/', include(admin.site.urls)),

    # auth endpoints
    url(r'^login/$', include('auth.urls')),
	url(r'^logout/$', include('auth.urls')),
	url(r'^register/$', include('auth.urls')),

	# apps for each 
    url(r'^teacher/', include('teachers.urls')),
    url(r'^student/', include('students.urls')),
    url(r'^parent/', include('parents.urls')),
    url(r'^school/', include('schools.urls')),

    # catch all (we'll forward them to login page)
    url(r'^$', include('auth.urls')),
)