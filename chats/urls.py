from django.urls import path, re_path
from .views import *
from .consumers import *

urlpatterns = [
    path("rooms/", MyRooms.as_view()),
    path("rooms/<str:room_key>/", ChatRoom.as_view()),
]

ws_urlpatterns = [
    re_path(r'ws/chats/(?p<room_name>\w+)/$', ChatConsumer.as_asgi())
]