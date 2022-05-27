from channels.generic.websocket import WebsocketConsumer
from time import sleep
import json


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        
        for i in range(10):
            self.send(json.dumps({'message': i}))
            sleep(1)
