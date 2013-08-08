from django.shortcuts import render, redirect
from auth.helpers import get_teacher_for_user
from schools.models import Term
from classes.models import Course
from classes.helpers import make_stub
from students.models import EnrolledStudent
import json


def dashboard(request):
    class_teacher = get_teacher_for_user(request.user)
    courses = Course.objects.filter(teacher=class_teacher)

    return render(request, 'teachers/dashboard.html', {"courses": courses})


def add_course(request):
    class_teacher = get_teacher_for_user(request.user)
    courses = Course.objects.filter(teacher=class_teacher)

    if request.method == 'POST':
        class_name = request.POST['course_name']
        class_stub = make_stub(class_name)
        class_id = request.POST['course_id']
        class_teacher = get_teacher_for_user(request.user)
        class_term = Term.objects.get(school=class_teacher.school)

        # make sure this course doesn't already exist (check via stub)
        stub_count = Course.objects.filter(stub=class_stub, teacher=class_teacher).count()

        if stub_count == 0:
            new_course = Course(
                name=class_name,
                stub=class_stub,
                course_id=class_id,
                teacher=class_teacher,
                term=class_term
            )
            new_course.save()

            # forward to the courses' add student view
            return redirect('/teacher/courses/'+class_stub+'/roster/add')

    return render(request, 'teachers/courses/add_course.html', {'courses': courses})


def view_course(request, course_stub):
    class_teacher = get_teacher_for_user(request.user)
    courses = Course.objects.filter(teacher=class_teacher)

    course = Course.objects.get(stub=course_stub, teacher=class_teacher)

    return render(request, 'teachers/courses/view_course.html', {'course': course, 'courses': courses})


def edit_course(request, course_stub):
    class_teacher = get_teacher_for_user(request.user)
    course = Course.objects.get(stub=course_stub, teacher=class_teacher)

    if request.method == 'POST':
        class_name = request.POST['course_name']
        class_stub = make_stub(class_name)
        class_id = request.POST['course_id']

        if course is not None:
            # make sure the new stub doesn't already exist
            stub_count = Course.objects.filter(stub=class_stub, teacher=class_teacher).count()

            if stub_count == 0:
                course.name = class_name
                course.stub = class_stub
                course.course_id = class_id
                course.save()

                return redirect('/teacher')

    return render(request, 'teachers/courses/edit_course.html', {'course': course})


def course_roster(request, course_stub):
    class_teacher = get_teacher_for_user(request.user)
    courses = Course.objects.filter(teacher=class_teacher)
    course = Course.objects.get(stub=course_stub, teacher=class_teacher)

    students_in_class = EnrolledStudent.objects.filter(course=course)

    return render(request, 'teachers/courses/course_roster.html', {
        'roster': students_in_class,
        'courses': courses,
        'course': course
    })


def add_students(request, course_stub):
    class_teacher = get_teacher_for_user(request.user)
    course = Course.objects.get(stub=course_stub, teacher=class_teacher)

    # grab the array of students
    if request.method == 'POST':
        students_json = json.loads(request.POST['students'])

        for student in students_json:
            new_student = EnrolledStudent(
                course=course,
                first_name=student['first_name'],
                last_name=student['last_name'],
                email=student['email']
            )
            new_student.save()

            # TODO: send email to student to join course

            return redirect('/teacher/courses/'+course.stub+'/roster')

    return render(request, 'teachers/courses/add_students.html')


def delete_student(request, student_id, course_stub):
    class_teacher = get_teacher_for_user(request.user)
    course = Course.objects.get(stub=course_stub, teacher=class_teacher)

    enrolled_student = EnrolledStudent.objects.get(pk=student_id, course=course)

    enrolled_student.delete()

    return redirect('/teacher/courses/'+course_stub)


def view_evaluation(request, course_stub, eval_id):
    class_teacher = get_teacher_for_user(request.user)
    courses = Course.objects.filter(teacher=class_teacher)
    course = Course.objects.get(stub=course_stub, teacher=class_teacher)

    return render(request, 'teachers/courses/evaluations.html', {'courses':courses, 'course':course})


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