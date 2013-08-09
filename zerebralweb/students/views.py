from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required


@permission_required('auth.needs_consent')
def consent(request):
    return render(request, 'students/consent.html')


@permission_required('auth.is_student')
def dashboard(request):
    return render(request, 'students/dashboard.html')


@permission_required('auth.is_student')
def all_goals(request):
    return render(request, 'students/goals/all_goals.html')


@permission_required('auth.is_student')
def view_goal(request, goal_id):
    return render(request, 'students/goals/view_goal.html')


@permission_required('auth.is_student')
def points(request):
    return render(request, 'students/points/overview.html')


@permission_required('auth.is_student')
def badges(request):
    return render(request, 'students/badges/overview.html')


@permission_required('auth.is_student')
def actionplans(request):
    return render(request, 'students/actionplans/overview.html')


@permission_required('auth.is_student')
def new_actionplan(request):
    return render(request, 'students/actionplans/new_actionplan.html')


@permission_required('auth.is_student')
def edit_actionplan(request, actionplan_id):
    return render(request, 'students/actionplans/edit_actionplan.html')


@permission_required('auth.is_student')
def join_course(request):
    return render(request, 'students/courses/join_course.html')


@permission_required('auth.is_student')
def settings(request):
    return render(request, 'students/settings/edit_profile.html')


@permission_required('auth.is_student')
def notifications(request):
    return render(request, 'notifications/students.html')