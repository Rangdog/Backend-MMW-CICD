from django.shortcuts import render

from rest_framework import permissions, generics
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from .serializers import *
from .models import *
from rest_framework.response import Response
from knox.models import AuthToken

from django.contrib.auth import get_user_model, authenticate
User = get_user_model()


class LoginAPIView(generics.CreateAPIView):
    permissions_classes = [permissions.AllowAny]
    serializer_class = LoginSerialiazer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user:
                _, token = AuthToken.objects.create(user)
                return Response(
                    {
                        "user": self.serializer_class(user).data,
                        "token": token
                    }
                )
            else:
                return Response({"error": "Invalid credentials"}, status=401)
        else:
            return Response(serializer.errors, status=400)
