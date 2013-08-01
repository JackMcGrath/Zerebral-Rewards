from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # auth endpoints
    url(r'^login', 'auth.views.login_view'),
    url(r'^register', 'auth.views.register_view'),
    url(r'^tos', 'auth.views.tos_view'),
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)