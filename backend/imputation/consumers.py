import json
from channels.generic.websocket import AsyncWebsocketConsumer

connected_clients = []

class AccuracyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept connection
        print("trying to connect..")
        await self.accept()
        connected_clients.append(self)

    async def disconnect(self, close_code):
        # Remove from connected clients
        connected_clients.remove(self)

    async def send_accuracy(self, accuracy):
        # Send accuracy to the client
        await self.send(text_data=json.dumps({
            'accuracy': accuracy
        }))
