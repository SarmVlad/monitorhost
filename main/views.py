from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from ipware.ip import get_ip

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

            content = {
                'next': request.GET['next'],
                'fail': True
            }
            return render(request, 'login.html', content)
    
    ip = get_ip(request)
    if ip is not None:
        print("We have an IP address for this client %s" %ip)
    else:
        print("We don't have an IP address for this client")
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

        try:
            user = User.objects.get(username=username)
            username_uni = False
        except User.DoesNotExist:
            username_uni = True

        try:
            user = User.objects.get(email=email)
            email_uni = False
        except User.DoesNotExist:
            email_uni = True

        if not username_uni or not email_uni:
            context = {
                'username': username_uni,
                'email': email_uni
            }
            return render(request, 'reg.html', context)

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                        password=password)
        user.send_hemail('Confirm your email', 'confirm_email.html')

        return render(request, 'message.html', {'text': 'Check your email'})
    else:
        context = {
            'username': True,
            'email': True
        }
        return render(request, 'reg.html', context)

def activate(request, username, code):
    user = User.objects.get(username=username)
    if code == user.activation_code and not user.activation_code == 'ACTIVATED':
        user.is_active = True
        user.activation_code = 'ACTIVATED'
        user.save()
        return render(request, 'message.html', {'text': 'Your account has been activated'})
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