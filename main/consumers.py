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
def ws_connect(message, chat_id = 9 ):

    print(chat_id)
    # Accept the incoming connection
    message.reply_channel.send({"accept": True})
    # Add them to the chat group
    Group("chat-%s" % chat_id).add(message.reply_channel)
    print('connected')


@channel_session_user
def ws_message(message, chat_id):
    user = models.User.objects.get(username=message.user.username)

    models.Chat.objects.get(id=chat_id).message_set.create(author=user, text=message['text'])
    Group("chat-%s" % chat_id).send({
        "text": '{"username" : "'+user.username+'", "date" : " ' +timezone.now().__str__()+' ", "text" : " ' +message['text']+ ' "}',
    })


@channel_session_user
def ws_disconnect(message, chat_id):
    Group("chat-%s" % chat_id).discard(message.reply_channel)
    print("disconnect")