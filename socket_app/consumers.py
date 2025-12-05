import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from socket_app.models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']  # e.g. nishatroom
        self.room_group_name = f"chat_{self.room_name}"  # MUST be consistent

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print(f"[CONNECTED] User joined room: {self.room_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(f"[DISCONNECTED] User left room: {self.room_name}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"[RECEIVED CMD] {data}")  # CMD-তে দেখাবে

        # Save message to DB
        await self.create_message(data)

        # Send to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',  # MUST match function name below
                'message': data
            }
        )

    async def chat_message(self, event):  # type name must match
        data = event['message']
        print(f"[SENT CMD] {data}")  # CMD log
        await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def create_message(self, data):
        room, _ = Room.objects.get_or_create(room_name=data['room_name'])
        Message.objects.create(room=room, sender=data['sender'], message=data['message'])
