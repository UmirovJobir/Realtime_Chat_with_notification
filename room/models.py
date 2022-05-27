from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class Room(models.Model):
    roomname = models.CharField(max_length=64)
    creator = models.ForeignKey(User, related_name='user_rooms', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='rooms')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.roomname


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    message = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created']
    
    def __str__(self):
        return str(self.created)


class Visit(models.Model):
    user = models.ForeignKey(User, related_name='user_visits', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='room_visits', on_delete=models.CASCADE)
    last_visit = models.DateTimeField()
