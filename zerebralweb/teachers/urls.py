from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # overview of all courses
    url(r'^dashboard', 'teachers.views.dashboard'),

    # add a new course
    url(r'^courses/add', 'teachers.views.add_course'),
    # view (and edit) an evaluation for a course
    url(r'^courses/(?P<course_id>\w+)/evaluations/(?P<eval_id>\w+)', 'teachers.views.view_evaluation'),
    # edit a course
    url(r'^courses/(?P<course_id>\w+)/edit', 'teachers.views.edit_course'),
    # add students to a course
    url(r'^courses/(?P<course_id>\w+)/roster/add', 'teachers.views.add_students'),
    # view students of a course
    url(r'^courses/(?P<course_id>\w+)/roster', 'teachers.views.course_roster'),
    # view stats and performance of a course
    url(r'^courses/(?P<course_id>\w+)', 'teachers.views.view_course'),


    # add a new goal
    url(r'^goals/add', 'teachers.views.add_goal'),
    # edit a goal
    url(r'^goals/(?P<goal_id>\w+)/edit', 'teachers.views.edit_goal'),
    # approve pending goal redemptions
    url(r'^goals/approvals', 'teachers.views.approve_goals'),
    # list showing all goals the teacher has created
    url(r'^goals', 'teachers.views.all_goals'),

    # view all pending action plans (option to approve or revise
    url(r'^actionplans', 'teachers.views.action_plans'),

    # edit teacher profile/site settings
    url(r'^settings', 'teachers.views.settings'),

    # teacher notifications
    url(r'^notifications', 'teachers.views.notifications'),


    # first view should always be dashboard
    url(r'^$', RedirectView.as_view(url='/teacher/dashboard')),
    url(r'^courses', RedirectView.as_view(url='/teacher/dashboard')),
)