from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django import forms





class StudentRegisterForm(forms.Form):
    school_id = forms.IntegerField()
    student_id = forms.IntegerField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=254)
    password = forms.CharField(max_length=100, min_length=4)
    confirm_password = forms.CharField(max_length=100, min_length=4)



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
            return render(request, 'auth/login.html', {error: 'Incorrect username or password.'})
        elif not user.is_active:
            # user's account is disabled
            return render(request, 'auth/login.html', {error: 'Your account has been disabled.'})

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
    return render(request, 'auth/login.html', {error: ''})


def register(request):
    if request.method == 'POST':
        # TODO
        pass

    return render(request, 'auth/register.html')