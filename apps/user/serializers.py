from rest_framework_simplejwt.tokens import RefreshToken

import common.serializers
from .models import User, LoginSessions
import common.code as c
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

"""
# 기존 시리얼라이저 
"""


class UserSerializer(common.serializers.CommonSerializer):
    enum_field = {
        "role": c.USER_TYPE,
    }

    class Meta:
        model = User
        # fields = '__all__'
        fields = ["id", "name", "username", "email", "description", "role",  "created_at", "updated_at"]


class LoginSessionsSerializer(TokenObtainPairSerializer):
    enum_field = {
        "role": c.USER_TYPE,
    }
    class Meta:
        model = LoginSessions
        fields = "__all__"
