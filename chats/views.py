import secrets
from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status as httpStatus
from django.db.models import Q
from api.models import Student, User
from chats.models import Messages, SingleChatRooms
from chats.serializers import SingleChatRoomsSerializer
from datetime import datetime
# Create your views here.

def generate_room_key(length=15):
    """
    Generate a random string of the specified length.
    Default length is 15 characters.
    """
    return secrets.token_urlsafe(length)

class MyRooms(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        all_users =  User.objects.all()
        listUsers = []
        for user in all_users:
            if  user != request.user and (user.user_type == 'student' or user.user_type == 'staff' or user.user_type == 'club'):
                # u = Student.objects.filter(user = request.user)
                listUsers.append({
                    "username" : user.username,
                    "id" : user.id
                })
        return Response(data=listUsers, status=httpStatus.HTTP_200_OK)
    
    def post(self, request):
        
        # for x in SingleChatRooms.objects.all():
        #     x.delete()

        sender_user = request.user
        receiver_user = User.objects.get(id=request.POST["receiver_user"])

        get_room = SingleChatRooms.objects.filter(Q(sender_user=sender_user , receiver_user=receiver_user) | Q(sender_user=receiver_user, receiver_user=sender_user))

        if get_room:
            room_key = get_room[0].room_key
            return Response(data={"room_key" : room_key}, status=httpStatus.HTTP_200_OK)
        else:
            room_key = generate_room_key()

            while True:
                if SingleChatRooms.objects.filter(room_key=room_key):
                    room_key = generate_room_key()
                else:
                    break
            
            # serializer = SingleChatRoomsSerializer(data = {"sender_user" : sender_user, "receiver_user" : receiver_user, "room_key" : room_key, "last_msg_time" : datetime.now() })
            # if serializer.is_valid():
            #     return Response(data={"room_key" : room_key}, status=httpStatus.HTTP_201_CREATED)
            # else:
            #     return Response(data={"response" : "error creating room"}, status=httpStatus.HTTP_400_BAD_REQUEST)
                
            room = SingleChatRooms(sender_user= sender_user, receiver_user=receiver_user,room_key= room_key)
            room.save()
            return Response(data={"room_key" : room.room_key}, status=httpStatus.HTTP_201_CREATED)
          
            
class ChatRoom(APIView):
    def get(self, request, room_key):
        sender_user = request.user
        # room = SingleChatRooms.objects.get(room_key= request.data["room_key"])
        print("this is the room name" , room_key)
        room = SingleChatRooms.objects.get(room_key= room_key)
        print("room is",room)
        if room.sender_user == sender_user:
            print("reciver", room.receiver_user)
            print("type", type(room.receiver_user))
            receiver_user = room.receiver_user
        else:
            receiver_user =room.sender_user
        
        msgs = []
        for msg in  Messages.objects.filter(Q(sender_user=sender_user.id, receiver_user=receiver_user.id) | Q(sender_user=receiver_user.id, receiver_user=sender_user.id)):
            msgs.append({
                "message" : msg.message,
                "isSender" : msg.sender_user == request.user
            })

        

        return Response(data={
            "messages" : msgs,
            # "receiver_name" : receiver_user.username,
            "revicer_id" : receiver_user.id,
            "sender_id" : sender_user.id
        }) 
        


