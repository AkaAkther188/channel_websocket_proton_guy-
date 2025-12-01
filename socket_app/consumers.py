from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from socket_app.models import *

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name= f"room_{self.scope['url_route'] ['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        


   # async def receive(self, text_data):
       # data = json.loads(text_data)
       # msg = data.get("message")

       # await self.send(text_data=json.dumps({
        #    "message": msg
       # }))

    async def disconnect(self, close_code):
      await self.channel_layer.group_discard(self.room_name, self.channel_name)
