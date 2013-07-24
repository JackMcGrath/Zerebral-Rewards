from django.shortcuts import render, redirect

def dashboard(request):
    return render(request, 'teachers/dashboard.html')