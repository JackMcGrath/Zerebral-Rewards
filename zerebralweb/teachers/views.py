from django.shortcuts import render, redirect
from auth.helpers import get_teacher_for_user
from schools.models import Term
from classes.models import Course
from classes.helpers import make_stub
from students.models import EnrolledStudent
from evaluations.models import Evaluation
from teachers.helpers import send_course_invite_email, get_current_week
import json
from django.contrib.auth.decorators import permission_required
from datetime import timedelta, date
from operator import itemgetter


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
def redirect_current_week(request, course_stub):
    class_teacher = get_teacher_for_user(request.user)
    course = Course.objects.get(stub=course_stub, teacher=class_teacher)

    current_week = get_current_week(course.term.begin_date, course.term.end_date)

    return redirect('/teacher/courses/' + course_stub + '/evaluations/' + str(current_week))


@permission_required('auth.is_teacher')
def view_evaluation(request, course_stub, week_no):
    class_teacher = get_teacher_for_user(request.user)
    courses = Course.objects.filter(teacher=class_teacher).order_by('name')
    course = Course.objects.get(stub=course_stub, teacher=class_teacher)
    students = EnrolledStudent.objects.filter(course=course).order_by('first_name', 'last_name')
    student_evals = []

    # calculate out weeks for term and send them to the template
    weeks = []
    current_week = course.term.begin_date
    week_count = 1

    while current_week < course.term.end_date:
        evals_for_this_week = (Evaluation.objects.filter(course=course, week=week_count, submitted=True).count() > 0)

        is_current_week = current_week <= date.today() <= (current_week + timedelta(days=7))

        weeks.append({
            'week_no': week_count,
            'week_start': str(current_week),
            'submitted': evals_for_this_week,
            'current': is_current_week
        })
        week_count += 1
        current_week += timedelta(days=7)

    # get all point categories
    point_categories = course.term.point_categories.all().order_by('name')

    # parse through students and evaluations and place combined results in student_evals
    for student in students:
        combined_student = {}
        combined_student['first_name'] = student.first_name
        combined_student['last_name'] = student.last_name

        # try to grab an evaluation if it exists
        try:
            student_eval = Evaluation.objects.get(student=student, week=week_no, submitted=True)
            combined_student['evaluation'] = {}
            combined_student['evaluation']['point_categories'] = []

            # return the student's assessments ordered by point_category name (abc)
            ordered_assesments = sorted(student_eval.assessments.all(), key=itemgetter('pg'))

            for assn in ordered_assesments:
                combined_student['evaluation']['point_categories'].append(assn)

            combined_student['evaluation']['grade_percent'] = student_eval.grade_percent
            combined_student['evaluation']['engagement_percent'] = student_eval.engagement_percent
            combined_student['evaluation']['note'] = student_eval.note
        except:
            pass

        student_evals.append(combined_student)

    # TODO: handle update to evaluation models
    if request.method == 'POST':
        pass

    return render(request, 'teachers/courses/evaluations.html', {
        'courses': courses,
        'course': course,
        'weeks': weeks,
        'point_categories': point_categories,
        'evals': student_evals
    })


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