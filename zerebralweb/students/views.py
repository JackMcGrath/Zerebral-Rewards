from django.shortcuts import render, redirect

def dashboard(request):
    return render(request, 'students/dashboard.html')

def consent(request):
    return render(request, 'students/consent.html')

def all_goals(request):
    return render(request, 'students/goals/all_goals.html')

def view_goal(request, goal_id):
    return render(request, 'students/goals/view_goal.html')

def points(request):
    return render(request, 'students/points/overview.html')

def badges(request):
    return render(request, 'students/badges/overview.html')

def actionplans(request):
    return render(request, 'students/actionplans/overview.html')

def new_actionplan(request):
    return render(request, 'students/actionplans/new_actionplan.html')

def edit_actionplan(request, actionplan_id):
    return render(request, 'students/actionplans/edit_actionplan.html')

def join_course(request):
    return render(request, 'students/courses/join_course.html')

def settings(request):
    return render(request, 'students/settings/edit_profile.html')

def notifications(request):
    return render(request, 'notifications/students.html')