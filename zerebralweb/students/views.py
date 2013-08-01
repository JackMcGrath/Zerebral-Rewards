from django.shortcuts import render, redirect

def dashboard(request):
    return render(request, 'students/dashboard.html')

def consent(request):
    return render(request, 'students/consent.html')