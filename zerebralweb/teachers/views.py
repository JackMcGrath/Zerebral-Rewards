from django.shortcuts import render, redirect
from auth.helpers import get_teacher_for_user
from schools.models import Term
from classes.models import Course
from classes.helpers import make_stub
from students.models import EnrolledStudent
from teachers.helpers import send_course_invite_email
import json
from django.contrib.auth.decorators import permission_required
from datetime import datetime, timedelta


@permission_required('auth.is_teacher')
def dashboard(request):
    class_teacher = get_teacher_for_user(request.user)
    courses = Course.objects.filter(teacher=class_teacher).order_by('name')

    return render(request, 'teachers/dashboard.html', {"courses": courses})


@permission_required('auth.is_teacher')
def add_course(request):
    class_teacher = get_teacher_for_user(request.user)
    courses = Course.objects.filter(teacher=class_teacher).order_by('name')
    terms = Term.objects.filter(school=class_teacher.school).order_by('begin_date')

    if request.method == 'POST':
        try:
            if request.POST['course_name'] == '' or request.POST['course_id'] == '':
                return render(request, 'teachers/courses/add_course.html', {
                    'courses': courses,
                    'terms': terms,
                    'error': 'Please enter a course name and ID.'
                })

            class_name = request.POST['course_name']
            class_stub = make_stub(class_name)
            class_id = request.POST['course_id']
            class_teacher = get_teacher_for_user(request.user)
            class_term = Term.objects.get(pk=int(request.POST['course_term']))

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
                return redirect('/teacher/courses/' + class_stub + '/roster/add')
            else:
                return render(request, 'teachers/courses/add_course.html', {
                    'courses': courses,
                    'terms': terms,
                    'error': 'Class name already exists.'
                })
        except:
            return render(request, 'teachers/courses/add_course.html', {
                'courses': courses,
                'terms': terms,
                'error': 'Could not create class. Please try again.'
            })

    return render(request, 'teachers/courses/add_course.html', {'courses': courses, 'terms': terms})


@permission_required('auth.is_teacher')
def view_course(request, course_stub):
    class_teacher = get_teacher_for_user(request.user)
    courses = Course.objects.filter(teacher=class_teacher).order_by('name')

    course = Course.objects.get(stub=course_stub, teacher=class_teacher)

    return render(request, 'teachers/courses/view_course.html', {'course': course, 'courses': courses})


@permission_required('auth.is_teacher')
def edit_course(request, course_stub):
    class_teacher = get_teacher_for_user(request.user)
    course = Course.objects.get(stub=course_stub, teacher=class_teacher)

    if request.method == 'POST':
        class_name = request.POST['course_name']
        class_stub = make_stub(class_name)
        class_id = request.POST['course_id']
        class_term = Term.objects.get(pk=int(request.POST['course_term']))

        if course is not None:
            # make sure the new stub doesn't already exist
            stub_count = Course.objects.filter(stub=class_stub, teacher=class_teacher).count()

            if stub_count == 0:
                course.name = class_name
                course.stub = class_stub
                course.term = class_term
                course.course_id = class_id
                course.save()

                return redirect('/teacher')
            else:
                return render(request, 'teachers/courses/edit_course.html', {
                    'course': course,
                    'error': 'Class name already exists.'
                })
        else:
            return render(request, 'teachers/courses/edit_course.html', {
                'course': course,
                'error': 'Course could not be found.'
            })

    return render(request, 'teachers/courses/edit_course.html', {'course': course})


@permission_required('auth.is_teacher')
def course_roster(request, course_stub):
    class_teacher = get_teacher_for_user(request.user)
    courses = Course.objects.filter(teacher=class_teacher).order_by('name')
    course = Course.objects.get(stub=course_stub, teacher=class_teacher)

    students_in_class = EnrolledStudent.objects.filter(course=course)

    return render(request, 'teachers/courses/course_roster.html', {
        'roster': students_in_class,
        'courses': courses,
        'course': course
    })


@permission_required('auth.is_teacher')
def add_students(request, course_stub):
    class_teacher = get_teacher_for_user(request.user)
    courses = Course.objects.filter(teacher=class_teacher).order_by('name')
    course = Course.objects.get(stub=course_stub, teacher=class_teacher)

    # grab the array of students
    if request.method == 'POST':
        try:
            students_json = json.loads(request.POST['students'])

            for student in students_json:
                new_student = EnrolledStudent(
                    course=course,
                    first_name=student['first_name'],
                    last_name=student['last_name'],
                    email=student['email']
                )
                new_student.save()

                # send email to student to join course
                invite_url = request.build_absolute_uri('/student/joincourse/'+new_student.join_code)
                student_name = new_student.first_name + ' ' + new_student.last_name
                send_course_invite_email(invite_url, student_name, course.name, new_student.email)

            return redirect('/teacher/courses/' + course.stub + '/roster')
        except:
            return render(request, 'teachers/courses/add_students.html', {
                'courses': courses,
                'course': course,
                'error': 'Error in student inputs.'
            })

    return render(request, 'teachers/courses/add_students.html', {'courses': courses, 'course': course})


@permission_required('auth.is_teacher')
def delete_student(request, student_id, course_stub):
    class_teacher = get_teacher_for_user(request.user)
    course = Course.objects.get(stub=course_stub, teacher=class_teacher)

    enrolled_student = EnrolledStudent.objects.get(pk=student_id, course=course)

    enrolled_student.delete()

    return redirect('/teacher/courses/' + course_stub)


@permission_required('auth.is_teacher')
def view_evaluation(request, course_stub, eval_id):
    class_teacher = get_teacher_for_user(request.user)
    courses = Course.objects.filter(teacher=class_teacher).order_by('name')
    course = Course.objects.get(stub=course_stub, teacher=class_teacher)

    # calculate out weeks for term and send them to the template
    weeks = []
    current_week = course.term.begin_date
    week_count = 1

    while current_week < course.term.end_date:
        weeks.append({week_count: str(current_week)})
        week_count += 1
        current_week += timedelta(days=7)

    if request.method == 'POST':
        pass
        # TODO: handle update to evaluation models

    return render(request, 'teachers/courses/evaluations.html', {'courses': courses, 'course': course, 'weeks': weeks})


@permission_required('auth.is_teacher')
def all_goals(request):
    return render(request, 'teachers/goals/all_goals.html')


@permission_required('auth.is_teacher')
def add_goal(request):
    return render(request, 'teachers/goals/add_goal.html')


@permission_required('auth.is_teacher')
def edit_goal(request, goal_id):
    return render(request, 'teachers/goals/edit_goal.html')


@permission_required('auth.is_teacher')
def approve_goals(request):
    return render(request, 'teachers/goals/approve_goals.html')


@permission_required('auth.is_teacher')
def action_plans(request):
    return render(request, 'teachers/actionplans/manage_plans.html')


@permission_required('auth.is_teacher')
def settings(request):
    return render(request, 'teachers/settings/edit_profile.html')


@permission_required('auth.is_teacher')
def notifications(request):
    return render(request, 'notifications/teachers.html')