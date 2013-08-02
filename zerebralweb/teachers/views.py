from django.shortcuts import render, redirect

def dashboard(request):
    return render(request, 'teachers/dashboard.html')



def add_course(request):
    return render(request, 'teachers/courses/add_course.html')

def view_course(request, course_id):
    return render(request, 'teachers/courses/view_course.html')

def edit_course(request, course_id):
    return render(request, 'teachers/courses/edit_course.html')

def course_roster(request, course_id):
    return render(request, 'teachers/courses/course_roster.html')

def add_students(request, course_id):
    return render(request, 'teachers/courses/add_students.html')

def view_evaluation(request, course_id, eval_id):
    return render(request, 'teachers/courses/evaluations.html')

def all_goals(request):
    return render(request, 'teachers/goals/all_goals.html')

def add_goal(request):
    return render(request, 'teachers/goals/add_goal.html')

def edit_goal(request, goal_id):
    return render(request, 'teachers/goals/edit_goal.html')

def approve_goals(request):
    return render(request, 'teachers/goals/approve_goals.html')

def action_plans(request):
    return render(request, 'teachers/actionplans/manage_plans.html')

def settings(request):
    return render(request, 'teachers/settings/edit_profile.html')

def notifications(request):
    return render(request, 'notifications/teachers.html')