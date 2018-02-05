from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from .forms import UploadImgForm, handle_uploaded_user_img
from monitorhost import settings
import os

#from ipware.ip import get_ip

from django.contrib.auth import get_user_model

from main.admin import UserCreationForm
from main.models import Chat, Server_template

User = get_user_model()

import datetime

def index(request):
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None

    servers = Server_template.objects.all()

    context = {
        'user' : user,
        'servers' : servers,
    }
    return render(request, 'minecraft-hosting.html', context)

def log_in(request):
    if request.method == 'POST':
        username = request.POST['inputEmail']
        password = request.POST['inputPassword']
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

    '''ip = get_ip(request)
    if ip is not None:
        print("We have an IP address for this client %s" %ip)
    else:
        print("We don't have an IP address for this client")'''
    content = {
        'next' : request.GET['next']
    }
    return render(request, 'login.html', content)

def register(request):
    if request.method == 'POST':
        inputEmail = request.POST['inputEmail']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        inputEmail = request.POST['inputEmail']
        password = request.POST['password2']

        try:
            user = User.objects.get(username=inputEmail)
            username_uni = False
        except User.DoesNotExist:
            username_uni = True

        try:
            user = User.objects.get(email=inputEmail)
            email_uni = False
        except User.DoesNotExist:
            email_uni = True

        if not username_uni or not email_uni:
            context = {
                'inputEmail': username_uni,
                'inputEmail': email_uni
            }
            return render(request, 'reg.html', context)

        user = User.objects.create_user(username=inputEmail, first_name=first_name, last_name=last_name, email=inputEmail,
                                        password=password)
        user.send_hemail('Confirm your email', 'confirm_email.html')

        return render(request, 'message.html', {'text': 'Check your email'})
    else:
        context = {
            'inputEmail': True,
            'inputEmail': True
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


def recovery(request):
    if request.method == 'POST':
        inputEmail = request.POST['inputEmail']
        try:
            user = User.objects.get(Q(username=inputEmail) | Q(email=inputEmail))
        except:
            return render(request, 'password_recovery.html', {'fail': True})

        if user.is_active == False:
            return render(request, 'password_recovery.html', {'fail': True})

        user.password_recovery()
        return render(request,'message.html', {'text': 'Вам на почту отправлена ссылка для восстановления пароля'})
    else:
        return render(request, 'password_recovery.html')

def change_pass(request, username, code):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        user.set_password(request.POST['password'])
        user.password_recovery_code = 'None'
        user.save()
        return render(request, 'message.html', {'text': 'Пароль изменен'})
    else:
        user = User.objects.get(username=username)
        if not user.password_recovery_code == code:
            return Http404()
        context = {
            'username': username,
            'code': code
        }
        return render(request, 'change_password.html', context)

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
    if request.method == 'POST':
        form = UploadImgForm(request.POST, request.FILES)
        # Если данные валидны
        if form.is_valid():
            # обрабатываем файл
            handle_uploaded_user_img(request.FILES['file'])
            user = request.user
            user.photo.delete()
            user.photo = os.path.normpath("%s%s%s%s%s" %(os.getcwd(),"/main", settings.MEDIA_URL, "profile_photo/",
                                                         request.FILES['file'].name))
            user.save()
            # перенаправляем на другую страницу
            return redirect('/panel/')
    form = UploadImgForm()
    context = {
        'user' : request.user,
        'img_form': form
    }
    return render(request, 'panel.html', context)

@login_required
def load_user_img(request):
    if request.method == 'POST':
        user = request.user
        #user.photo = request.FILES['file']
        #user.save()
        print(request.FILES.items())
    return redirect('/')

@login_required
def chats(request):
    chat_list = request.user.chat_set.all()
    chats = []
    for chat in chat_list:
        chats.append( {
            'title' : chat.users.exclude(username=request.user.username)[0].username,
            'chat' : chat
        })

    context = {
        'user': request.user,
        'chats' : chats,
    }
    return render(request, 'chats.html', context)

@login_required
def chat(request, id=None):
    chat = Chat.objects.get(pk=id)
    messages = chat.message_set.order_by('date')
    context = {
        'messages' : messages,
        'chat_id' : id,
        'user' : request.user,
    }
    return render(request,'chat.html', context)

@login_required
def profile(request, id=None):
    context = {
        'user' : request.user,
    }
    return render(request,'profile.html', context)


@login_required
def servers(request):
    user_servers = request.user.server_set.all()
    context = {
        'servers' : user_servers,
    }
    return render(request, 'servers.html', context)


@login_required
def servers_for_sale(request):
    servers = Server_template.objects.all()
    context = {
        'servers': servers,
    }
    return render(request, 'servers_for_sale.html', context)


@login_required
def buy_server(request, id=None):
    server_template = Server_template.objects.get(pk=id)
    user = request.user
    if (user.money - server_template.price) >= 0:
        user.money -= server_template.price
        user.server_set.create(
            processor=server_template.processor,
            ram = server_template.ram,
            disk = server_template.disk,
            price = server_template.price,
            name = server_template.name,
        )
        user.save()
        return redirect("/panel/servers/")
    return render(request, "message.html", {'text' : "Недостаточно средств"})
