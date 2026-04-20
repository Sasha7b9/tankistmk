import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ImageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("image_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("image_updates", self.channel_name)

    async def send_image(self, event):
        await self.send(text_data=json.dumps({
            'filename': event['filename']
        }))
