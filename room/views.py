from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import viewsets, generics, mixins
from rest_framework import permissions
import json

from .models import Room, Message, Visit
from .serializers import RoomSerializer, MessageSerializer
from .permissions import IsOwnerOrReadOnly, ActionBasedPermission


class RoomViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        permissions.IsAuthenticated: ['create'],
        IsOwnerOrReadOnly: ['destroy', 'partial_update'],
        permissions.AllowAny: ['retrieve', 'list'] #Temporary permission
    }
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class MessageViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        permissions.IsAuthenticated: ['create'],#Temporaru permission
        IsOwnerOrReadOnly: ['destroy', 'partial_update'],
        permissions.AllowAny: ['retrieve', 'list'] #Temporary permission
    }
    
    def perform_create(self, serializer):
        
        """room = serializer.validated_data['room']
        try:
            visit = Visit.objects.get(user=self.request.user, room=room)
            visit.last_visit = now()
        except:
            visit = Visit.objects.create(user=self.request.user, room=room, last_visit=now())"""
        #print('Visit user: ', visit.user, ' room ', visit.room, ' last_visit ', visit.last_visit)
        
        serializer.save(user=self.request.user)


class RoomListView(ListView):
    template_name = 'rooms.html'
    model = Room
    
    def get_context_data(self,**kwargs):
        context = super(RoomListView,self).get_context_data(**kwargs)
        
        context['room_messages'] = []
        context['len_messages'] = []
        
        for obj in context['object_list']:
            print('Context: ', obj.roomname)
            room_name = obj.roomname
        
            user = self.request.user
            
            context['room_messages'] += [room_name]
            
            try:
                room = Room.objects.get(roomname=room_name)
                try:
                    visit = Visit.objects.filter(user=user, room=room).first()
                    messages = Message.objects.filter(room=room, created__gt=visit.last_visit)
                    context['len_messages'] += [len(messages)]
                except:
                    context['len_messages'] += [0]
            except:
                print('Room was not found 2')
        
        #context['picture'] = Picture.objects.filter(your_condition)
        return context
 

def room(request, room_name):
    
    context = {'room_name': room_name}
    
    try:
        room = Room.objects.get(roomname=room_name)
        messages = Message.objects.filter(room=room)
        context['messages'] = []
        for msg in messages:
            context['messages'] += [msg.message]
    except:
        print('Room was not found 3')
    
    return render(request, 'chat.html', context)
