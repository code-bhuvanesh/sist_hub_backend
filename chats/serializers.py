from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import *



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ("sender_user", "receiver_user", "msg")

class SingleChatRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleChatRooms
        fields = ("sender_user", "receiver_user", "room_key")

        validators = [
            UniqueTogetherValidator(
                queryset=SingleChatRooms.objects.all(),
                fields=[ "sender_user", "receiver_user", 'room_key']
            )
        ]
        