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
        "user": c.USER_TYPE,
    }

    class Meta:
        model = User
        fields = '__all__'

class UserRegisterSerializer(common.serializers.CommonSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSessionsSerializer(TokenObtainPairSerializer):

    class Meta:
        model = LoginSessions
        fields = "__all__"

class UserLoginSerializer(serializers.ModelSerializer):
    username = LoginSessionsSerializer(many=True, read_only=True)  # 외래키로 연결된 테이블 정보 추가

    class Meta:
        model = User
        # fields = "__all__"
        fields = ["name", "username", "email", "role",  "created_at", "updated_at", 'username']
