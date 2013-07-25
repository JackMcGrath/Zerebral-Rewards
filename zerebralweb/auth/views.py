from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login




def login(request):
    if request.user.is_authenticated():
        # grab the user object
        user = request.user
    # we need to check login credentials
    elif request.method == 'POST':
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
            login(username=request.POST['username'], password=request.POST['password'])

    # NOTE: superadmins will ALWAYS have EVERY permission (even if they don't exist!)
    if request.user.is_active and request.user.is_superuser:
        return redirect('/admin')
    elif request.user.has_perm('auth.is_teacher'):
        return redirect('/teacher')
    elif request.user.has_perm('auth.is_student'):
        return redirect('/student')      

    # no permissions? not logged in? send them to login page
    return render(request, 'auth/login.html', {'error': ''})


def register(request):
    if request.method == 'POST':
        if request.POST['type'] == 'teacher':
            pass
        elif request.POST['type'] == 'student':
            pass

    return render(request, 'auth/register.html')