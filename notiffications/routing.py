from django.urls import path

from .consumers import WSConsumer


ws_urlpatterns = [
    path('ws/notiffications/', WSConsumer.as_asgi()),
]
