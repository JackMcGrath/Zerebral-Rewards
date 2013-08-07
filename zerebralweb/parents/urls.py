from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # consent view
    url(r'^consent/(?P<consent_token>\w+)', 'parents.views.consent'),

    # all other parent urls
    url(r'^$', RedirectView.as_view(url='/')),
)