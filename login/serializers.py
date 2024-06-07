from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginSerialiazer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # mục đích của việc này là không cho password bị phơi ra
        ret.pop("password", None)
        return ret
