from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from schools.models import School
from django.contrib.auth.decorators import login_required
from auth.models import ZerebralUser
from django.contrib.auth.models import User, Permission
from teachers.models import Teacher
from students.models import Student
from auth.helpers import *
from django.db import IntegrityError
from parents.models import Parent


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

    # grab all schools to pass onto registration form
    schools = School.objects.all()

    if request.method == 'POST':
        if request.POST['type'] == 'teacher':
            try:
                new_user = User.objects.create_user(
                    username=request.POST['username'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    password=request.POST['password'],
                    email=request.POST['email']
                )
            except IntegrityError as e:
                if str(e) == 'column username is not unique':
                    return render(request, 'auth/register.html', {
                        'schools': schools,
                        'error': 'Username is already taken.'
                    })
                else:
                    return render(request, 'auth/register.html', {
                        'schools': schools,
                        'error': 'Registration error. Please try again.'
                    })

            needs_tos = Permission.objects.get(codename='needs_tos')
            new_user.user_permissions.add(needs_tos)
            new_user.save()
            teacher_name = new_user.first_name + ' ' + new_user.last_name

            # grab the selected school model
            home_school = School.objects.get(pk=request.POST['school'])

            new_teacher = Teacher(school=home_school)
            new_teacher.save()

            z_user = ZerebralUser(user=new_user, teacher=new_teacher)
            z_user.save()

            new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, new_user)

            # send the welcome email
            send_teacher_welcome_email(teacher_name, new_user.email)

            return redirect('/accounts/tos')
        elif request.POST['type'] == 'student':
            try:
                new_user = User.objects.create_user(
                    username=request.POST['username'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    password=request.POST['password'],
                    email=request.POST['email']
                )
            except IntegrityError as e:
                if str(e) == 'column username is not unique':
                    return render(request, 'auth/register.html', {
                        'schools': schools,
                        'error': 'Username is already taken.'
                    })
                else:
                    return render(request, 'auth/register.html', {
                        'schools': schools,
                        'error': 'Registration error. Please try again.'
                    })

            needs_tos = Permission.objects.get(codename='needs_tos')
            new_user.user_permissions.add(needs_tos)
            new_user.save()
            student_name = new_user.first_name + ' ' + new_user.last_name

            # grab the existing parent or create a new one
            try:
                new_parent = Parent.objects.get(email__iexact=request.POST['parent_email'])
            except:
                new_parent = None

            try:
                if new_parent is None:
                    new_parent = Parent(
                        email=request.POST['parent_email'],
                        first_name=request.POST['parent_first_name'],
                        last_name=request.POST['parent_last_name']
                    )
                    new_parent.save()

                new_student = Student(
                    parent_token=generate_token(50),
                    parent=new_parent
                )
                new_student.save()
            except:
                new_user.delete()
                return render(request, 'auth/register.html', {
                    'schools': schools,
                    'error': "Please enter your parent's contact info."
               })

            # send email to parent for consent
            send_consent_email(
                request.build_absolute_uri('/parent/consent/'+new_student.parent_token),
                student_name,
                new_parent.email
            )

            z_user = ZerebralUser(user=new_user, student=new_student)
            z_user.save()

            new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, new_user)

            # send the welcome email
            send_student_welcome_email(student_name, new_user.email)

            return redirect('/accounts/tos')



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
                    student_perm = Permission.objects.get(codename='is_student')
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