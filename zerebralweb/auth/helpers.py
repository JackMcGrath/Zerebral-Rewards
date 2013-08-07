from auth.models import ZerebralUser
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def get_zerebral_user_for_django_user(user):
    return ZerebralUser.objects.get(user=user)


def get_django_user_for_student(student):
    z_user = ZerebralUser.objects.get(student=student)
    return z_user.user


def is_student(user):
    z_user = get_zerebral_user_for_django_user(user)

    if z_user.student is not None:
        return True

    return False


def is_teacher(user):
    z_user = get_zerebral_user_for_django_user(user)

    if z_user.teacher is not None:
        return True

    return False


def get_student_for_user(user):
    z_user = get_zerebral_user_for_django_user(user)
    return z_user.student


def get_teacher_for_user(user):
    z_user = get_zerebral_user_for_django_user(user)
    return z_user.teacher


def generate_token(length):
    return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(length))


def send_consent_email(consent_url, student_name, parent_email):
    plaintext = get_template('email/parental_consent.txt')
    htmly = get_template('email/parental_consent.html')

    d = Context({'consent_url': consent_url, 'student_name': student_name})

    subject, from_email, to = 'Zerebral Student Consent Request', 'noreply@zerebral.com', parent_email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_student_welcome_email(name, email):
    plaintext = get_template('email/welcome_student.txt')
    html = get_template('email/welcome_student.html')

    d = Context({'name': name})

    subject, from_email, to = 'Welcome to Zerebral!', 'noreply@zerebral.com', email
    text_content = plaintext.render(d)
    html_content = html.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_teacher_welcome_email(name, email):
    plaintext = get_template('email/welcome_teacher.txt')
    html = get_template('email/welcome_teacher.html')

    d = Context({'name': name})

    subject, from_email, to = 'Welcome to Zerebral!', 'noreply@zerebral.com', email
    text_content = plaintext.render(d)
    html_content = html.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()