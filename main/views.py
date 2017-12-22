from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
#import

from django.contrib.auth import get_user_model

from main.admin import UserCreationForm

User = get_user_model()


def index(request):
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None

    context = {
        'user' : user,
    }
    return render(request, 'index.html', context)

def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'])
        else:
            return HttpResponse('ERROR')

    content = {
        'next' : request.GET['next']
    }
    return render(request, 'login.html', content)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password2']

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                        password=password)
        user.send_hemail('Confirm your email', 'confirm_email.html')
        return render(request, 'messange.html', {'text': 'Check your email'})
    else:
        return render(request, 'reg.html')

def activate(request, username, code):
    user = User.objects.get(username=username)
    if code == user.activation_code and not user.activation_code == 'ACTIVATED':
        user.is_active = True
        user.activation_code = 'ACTIVATED'
        user.save()
        return render(request, 'messange.html', {'text': 'Your account has been activated'})
    else:
        return Http404()


def check(request):
    value = request.GET['value']
    try:
        user = User.objects.get(username=value)
        return HttpResponse('The username already exists')
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=value)
            return HttpResponse('The email already exists')
        except User.DoesNotExist:
            return HttpResponse('OK')

def log_out(request):
    logout(request)
    return redirect('/')

@login_required
def panel(request):
    return render(request, 'panel.html')