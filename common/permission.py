from django.urls import resolve
from rest_framework import permissions

from apps.user.models import User
from common.code import USER_TYPE
from common.enum import E


class IsAuthorUpdateOrReadonly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        if request.method == 'GET':
            return True

        if request.method == 'DELETE':
            if request.user.role == str(USER_TYPE.ADMIN):
                return True
            elif request.user.role == str(USER_TYPE.USER):
                return request.user.username == request.data.get('username')

        # 'update' 요청은 본인 또는 관리자만 가능
        if request.method in ['PUT', 'PATCH']:
            user_role = request.data.get('role')

            if request.user.role == str(USER_TYPE.ADMIN):
                return True
            elif request.user.role == str(USER_TYPE.USER):
                if user_role is not None:
                    return False
                user_email = request.data.get('email')
                try:
                    target_user = User.objects.get(email=user_email)
                    return request.user.username == target_user.username
                except User.DoesNotExist:
                    return False

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True


        return False


class AdminOrOwnerPermission:
    def has_permission(self, request, view):
        if request.user.role == str(USER_TYPE.ADMIN):
            return True
        elif request.user.role == str(USER_TYPE.USER):
            return request.user.username == request.data.get('username')
        return False
