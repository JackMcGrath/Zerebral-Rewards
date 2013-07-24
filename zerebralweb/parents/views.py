from django.shortcuts import render_to_response, redirect

def dashboard(request):
    return render_to_response('parents/dashboard.html')