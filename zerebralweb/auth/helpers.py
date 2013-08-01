from auth.models import ZerebralUser
import random


def get_zerebral_user_for_django_user(user):
    return ZerebralUser.objects.get(user=user)


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