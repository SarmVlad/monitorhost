from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

def index(request):
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None

    context = {
        'user' : user,
    }
    return render(request, 'index.html', context)

#Method for login
def sign_in(request):
    return None

def login(request):
    return render(request, 'login.html')

#Method for reg
def reg(request):
    return None

def register(request):
    return  render(request, 'reg.html')

@login_required
def panel(request):
    return render(request, 'panel.html')


def logout(request):
    logout(request)
    return render(request, 'login.html')