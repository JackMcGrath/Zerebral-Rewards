from django.shortcuts import render, redirect


def consent(request, consent_token):
    return render(request, 'parents/consent.html')