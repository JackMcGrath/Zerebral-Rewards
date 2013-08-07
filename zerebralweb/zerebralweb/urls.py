from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # enable admin
    url(r'^admin/', include(admin.site.urls)),

    # auth endpoints
    url(r'^accounts/', include('auth.urls')),

    # apps for each
    url(r'^teacher/', include('teachers.urls')),
    url(r'^student/', include('students.urls')),
    url(r'^parent/', include('parents.urls')),

    # catch all (acts as a router to proper dashboard)
    url(r'^$', 'auth.views.home_view'),
)