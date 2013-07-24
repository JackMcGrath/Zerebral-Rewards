from django.shortcuts import render, redirect
from django.contrib.auth import logout


def login(request):
    if request.user.is_authenticated():
        # what are you?

        # NOTE: superadmins will ALWAYS have EVERY permission (even if they don't exist!)
        if request.user.is_active and request.user.is_superuser:
            return redirect('/admin')
        elif request.user.has_perm('auth.is_school'):
            return redirect('/school')
        elif request.user.has_perm('auth.is_teacher'):
            return redirect('/teacher')
        elif request.user.has_perm('auth.is_parent'):
            return redirect('/parent')
        elif request.user.has_perm('auth.is_student'):
            return redirect('/student')

    # no permissions? not logged in? send them to login page
    return render(request, 'auth/login.html')


def register(request):
    return render(request, 'auth/register.html')