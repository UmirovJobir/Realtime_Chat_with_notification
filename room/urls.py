from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from .views import RoomViewSet, MessageViewSet, RoomListView, room


router = DefaultRouter()
router.register('room', RoomViewSet)
router.register('message', MessageViewSet)

urlpatterns = [
    path('room-list/', RoomListView.as_view()),
    path('room-chat/<str:room_name>/', room),
]

urlpatterns += router.urls
