from django.shortcuts import render
#from django.contrib.auth.models import User
from rest_framework import generics, views, permissions, status
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response

from django.contrib.auth import get_user_model
User = get_user_model()

from .serializers import RegisterSerializer, LogoutSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LogoutView(views.APIView):
    serializer_class = LogoutSerializer
    permissions = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status.HTTP_204_NO_CONTENT)
