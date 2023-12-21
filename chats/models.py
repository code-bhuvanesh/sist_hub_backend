from django.db import models

from django.contrib.auth.models import Group, Permission
from api.models import User


#models related to chats
class  Messages(models.Model):
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    receviced = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)


class SingleChatRooms(models.Model):
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="room_creator")
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="room_user")
    last_msg_time = models.DateTimeField(auto_now_add=True)
    room_key = models.TextField(max_length=20, unique=True)

   