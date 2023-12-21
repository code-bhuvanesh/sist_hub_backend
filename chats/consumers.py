import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from api.models import User

from chats.models import Messages

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#         print("client accepted")
    
#     def disconnect(self, code):
#         pass

#     def receive(self, text_data=None, bytes_data=None):
#         return super().receive(text_data, bytes_data)
        
        
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_key']
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def save_messages(self, message, sender, receiver):
        sender_user = User.objects.get(id=sender)
        receiver_user = User.objects.get(id=receiver)
        Messages.objects.create(message=message, sender_user=sender_user, receiver_user=receiver_user).save()

    def receive(self, text_data):
        print(text_data) 
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]
        receiver = text_data_json["receiver"]
        sender_name = text_data_json["sender_name"]
        self.save_messages(message, sender, receiver)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'chat_message',
                'message' : message,
                'sender' : sender,
                'receiver' : receiver,
                'sender_name' :sender_name
            }
        )
        
    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        sender_name = event['sender_name']

        self.send(text_data=json.dumps({
            'message' : message,
            'sender' : sender,
            'receiver' : receiver,
            'sender_name' : sender_name
        }))

