from django.shortcuts import render, redirect

def dashboard(request):
    return render(request, 'schools/dashboard.html')