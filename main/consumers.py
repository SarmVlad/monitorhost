from channels.auth import channel_session_user, channel_session_user_from_http
from django.http import HttpResponse
from channels.handler import AsgiHandler, AsgiRequest
import json
from channels.channel import Group
from django.utils import timezone

from main import models


#Можно оптимизировать сохраняя в message данные при первом подключении

def http_request_consumer(message):
    response = HttpResponse('Hello world! You asked for %s' % message.content['path'])
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)


@channel_session_user_from_http
def ws_connect(message):
    # Accept the incoming connection
    message.reply_channel.send({"accept": True})
    # Add them to the chat group
    Group("chat").add(message.reply_channel)
    print("connect")


@channel_session_user
def ws_message(message):
    mess = json.loads(message.content['text'])
    user = models.User.objects.get(username=message.user.username)
    message_db = models.Message.objects.create(author=user, text=mess['text'], chat=models.Chat.objects.get(id=6))
    #models.Chat.objects.get(id=6).message_set.create(author=user, text=mess['text'])
    Group("chat").send({
        "text": '{"username" : " ' +user.username+ ' ", "date" : " ' +message_db.date.__str__()+' ", "text" : " ' +mess['text']+ ' "}',
    })


@channel_session_user
def ws_disconnect(message):
    Group('chat').discard(message.reply_channel)
    print("disconnect")