from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # overview of all courses
    url(r'^dashboard', 'students.views.dashboard'),

    # displayed when a student has not yet received parental consent
    url(r'^consent', 'students.views.consent'),

    # goal details page (can redeem a goal from here)
    url(r'^goals/(?P<goal_id>\w+)', 'students.views.view_goal'),

    # show all goals currently available to student
    url(r'^goals', 'students.views.all_goals'),

    # point overview and history
    url(r'^points', 'students.views.points'),

    # all earned badges
    url(r'^badges', 'students.views.badges'),

    # edit/revise an existing action plan
    url(r'^actionplans/(?P<actionplan_id>\w+)/edit', 'students.views.edit_actionplan'),

    # create a new action plan
    url(r'^actionplans/new', 'students.views.new_actionplan'),

    # all active action plans
    url(r'^actionplans', 'students.views.actionplans'),

    # join courses using course codes
    url(r'^joincourse', 'students.views.join_course'),

    # edit student profile/site settings
    url(r'^settings', 'students.views.settings'),

    # student notifications
    url(r'^notifications', 'students.views.notifications'),


    # first view should always be dashboard
    url(r'^$', RedirectView.as_view(url='/student/dashboard')),
)