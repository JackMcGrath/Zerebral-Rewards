from django.shortcuts import render, redirect
from students.models import Student
from django.contrib.auth.models import Permission
from auth.models import ZerebralUser
from auth.helpers import get_django_user_for_student


def consent(request, consent_token):
    student = Student.objects.get(parent_token=consent_token)
    d_user = get_django_user_for_student(student)
    student_full_name = d_user.first_name + ' ' + d_user.last_name

    if request.method == 'POST':
        if request.POST['digital_signature'] is not None and request.POST['digital_signature'] != '':
            if student is not None:
                student.consent_from_parent = True
                student.consent_signed_by = request.POST['digital_signature']
                student.save()

                zu = ZerebralUser.objects.get(student=student)

                # make the student active if they've already accepted the TOS
                if zu.tos_accepted is True:
                    consent_perm = Permission.objects.get(codename='needs_consent')
                    d_user.user_permissions.remove(consent_perm)
                    student_perm = Permission.objects.get(codename='is_student')
                    d_user.user_permissions.add(student_perm)
                    d_user.save()


    return render(request, 'parents/consent.html', {'student_name': student_full_name})