from channels.routing import route

from main import consumers

channel_routing = [
    route("websocket.connect", consumers.ws_connect, path=r"^/chat/(?P<chat_id>[0-9]+)/$"),
    route("websocket.receive", consumers.ws_message, path=r"^/chat/(?P<chat_id>[0-9]+)/$"),
    route("websocket.disconnect", consumers.ws_disconnect, path=r"^/chat/(?P<chat_id>[0-9]+)/$"),
]