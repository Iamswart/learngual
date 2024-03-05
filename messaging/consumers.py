import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.recipient_id = self.scope['url_route']['kwargs']['recipient_id']

        self.room_name = f"chat_{min(self.sender_id, self.recipient_id)}_{max(self.sender_id, self.recipient_id)}"
        
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        await self.save_message(self.sender_id, self.recipient_id, message)
        
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.sender_id 
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    @database_sync_to_async
    def save_message(self, sender_id, recipient_id, message):
        sender = User.objects.get(id=sender_id)
        recipient = User.objects.get(id=recipient_id)
        Message.objects.create(
            sender=sender,
            recipient=recipient,
            content=message
        )
