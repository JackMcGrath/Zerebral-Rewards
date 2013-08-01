from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from schools.models import School
from django.contrib.auth.decorators import login_required




def home_view(request):
    if request.user.is_authenticated():
        # NOTE: superadmins will ALWAYS have EVERY permission (even if they don't exist!)
        if request.user.is_active and request.user.is_superuser:
            return redirect('/admin')
        elif request.user.has_perm('auth.is_teacher'):
            return redirect('/teacher')
        elif request.user.has_perm('auth.is_student'):
            return redirect('/student')

    return redirect('/accounts/login')



def login_view(request):
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
    if request.method == 'POST':
        if request.POST['type'] == 'teacher':
            return redirect('/accounts/tos')
        elif request.POST['type'] == 'student':
            return redirect('/accounts/tos')

    schools = School.objects.all()

    return render(request, 'auth/register.html', {'schools': schools})

@login_required
def tos_view(request):
    if request.method == 'POST':
        if request.POST['tos_accepted'] == 'yes':
            # TODO: update the user showing that they have accepted the TOS
            return redirect('/')

    return render(request, 'auth/tos.html')