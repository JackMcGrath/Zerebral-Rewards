from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from schools.models import School, Term, PointCategory
from django.contrib.auth.decorators import login_required
from auth.models import ZerebralUser
from django.contrib.auth.models import User, Permission
from teachers.models import Teacher
from students.models import Student
from auth.helpers import *
from datetime import datetime, timedelta


def home_view(request):
    if request.user.is_authenticated:
        # NOTE: superadmins will ALWAYS have EVERY permission (even if they don't exist!)
        if request.user.is_active and request.user.is_superuser:
            return redirect('/admin')
        elif request.user.has_perm('auth.is_teacher'):
            return redirect('/teacher')
        elif request.user.has_perm('auth.is_student'):
            return redirect('/student')
        elif request.user.has_perm('auth.needs_tos'):
            return redirect('/accounts/tos')
        elif request.user.has_perm('auth.needs_consent'):
            return redirect('/student/consent')

    return redirect('/accounts/login')



def login_view(request):
    # make sure users that are logged in can't reach this
    if request.user.is_authenticated and request.user.is_active:
        return redirect('/')

    if request.method == 'POST':
        try:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
        except:
            user = None

        if user is None:
            # incorrect username/password
            return render(request, 'auth/login.html', {'error': 'Incorrect username or password.'})
        elif not user.is_active:
            # user's account is disabled
            return render(request, 'auth/login.html', {'error': 'Your account has been disabled.'})
        else:
            # login is good
            login(request, user)
            return redirect('/')

    # send them to login page
    return render(request, 'auth/login.html')


def register_view(request):
    # make sure users that are logged in can't reach this
    if request.user.is_authenticated and request.user.is_active:
        return redirect('/')

    if request.method == 'POST':
        if request.POST['type'] == 'teacher':
            new_user = User.objects.create_user(
                username=request.POST['username'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                password=request.POST['password'],
                email=request.POST['email']
            )

            needs_tos = Permission.objects.get(codename='needs_tos')
            new_user.user_permissions.add(needs_tos)
            new_user.save()

            # grab the selected school model
            home_school = School.objects.get(pk=request.POST['school'])

            # count how many terms exist for the teacher's school
            term_count = Term.objects.filter(school=home_school).count()
            # we need to create a new term for this school
            if term_count < 1:
                attendance = PointCategory.objects.get(name='Attendance')
                effort = PointCategory.objects.get(name='Effort')
                citizenship = PointCategory.objects.get(name='Citizenship')
                participation = PointCategory.objects.get(name='Participation')

                new_term = Term(
                    school=home_school,
                    begin_date=datetime.now(),
                    end_date=(datetime.now()+timedelta(days=365))
                )
                new_term.save()
                new_term.point_categories.add(attendance, effort, citizenship, participation)
                new_term.save()

            new_teacher = Teacher(school=home_school)
            new_teacher.save()

            z_user = ZerebralUser(user=new_user, teacher=new_teacher)
            z_user.save()

            new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, new_user)

            return redirect('/accounts/tos')
        elif request.POST['type'] == 'student':
            new_user = User.objects.create_user(
                username=request.POST['username'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                password=request.POST['password'],
                email=request.POST['email']
            )

            needs_tos = Permission.objects.get(codename='needs_tos')
            new_user.user_permissions.add(needs_tos)
            new_user.save()

            new_student = Student(parent_email=request.POST['parent_email'], parent_token=generate_token(50))
            new_student.save()

            # TODO: send email to parent for consent

            z_user = ZerebralUser(user=new_user, student=new_student)
            z_user.save()

            new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, new_user)

            return redirect('/accounts/tos')

    schools = School.objects.all()

    return render(request, 'auth/register.html', {'schools': schools})


@login_required
def tos_view(request):
    # check if they have already accepted the TOS
    z_user = get_zerebral_user_for_django_user(request.user)
    if z_user.tos_accepted:
        return redirect('/')

    if request.method == 'POST':
        if request.POST['tos_accepted'] == 'yes':
            if is_teacher(request.user):
                # update permissions
                needs_tos = Permission.objects.get(codename='needs_tos')
                teacher_perm = Permission.objects.get(codename='is_teacher')
                request.user.user_permissions.remove(needs_tos)
                request.user.user_permissions.add(teacher_perm)
                request.user.save()

                # update ZerebralUser
                z_user.tos_accepted = True
                z_user.save()
            elif is_student(request.user):
                # update permissions
                needs_tos = Permission.objects.get(codename='needs_tos')
                request.user.user_permissions.remove(needs_tos)

                # change status to needs_consent if it's a student and they haven't yet received it
                if get_student_for_user(request.user).consent_from_parent:
                    student_perm = Permission.objects.get(codename='is_teacher')
                    request.user.user_permissions.add(student_perm)
                else:
                    consent_perm = Permission.objects.get(codename='needs_consent')
                    request.user.user_permissions.add(consent_perm)
                request.user.save()

                # update ZerebralUser
                z_user.tos_accepted = True
                z_user.save()

            return redirect('/')

    return render(request, 'auth/tos.html')