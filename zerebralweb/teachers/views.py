from django.shortcuts import render, redirect
from auth.helpers import get_teacher_for_user
from schools.models import Term
from classes.models import Course

def dashboard(request):
    return render(request, 'teachers/dashboard.html')

def add_course(request):
    if request.method == 'POST':
        class_name = request.POST['course_name']
        class_id = request.POST['course_id']
        class_teacher = get_teacher_for_user(request.user)
        class_term = Term.objects.get(school=class_teacher.school)

        new_course = Course(
            name=class_name,
            course_id=class_id,
            teacher=class_teacher,
            term=class_term
        )
        new_course.save()

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