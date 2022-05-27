from rest_framework import serializers

from .validators import LessThanValidator, GreaterThanValidator
from .models import Room, Message


class RoomSerializer(serializers.ModelSerializer):
    roomname = serializers.CharField(validators=[LessThanValidator(1), GreaterThanValidator(64)])
    creator = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Room
        fields = ['roomname', 'creator', 'users']


class MessageSerializer(serializers.ModelSerializer):
    message = serializers.CharField(validators=[LessThanValidator(1), GreaterThanValidator(256)])
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Message
        fields = ['message', 'room', 'user']
