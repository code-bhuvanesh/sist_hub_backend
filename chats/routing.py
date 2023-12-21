from django.urls import re_path
from .consumers import *

ws_urlpatterns = [
    re_path(r"^ws/chats/(?P<room_key>\w+)/$", ChatConsumer.as_asgi())
]   