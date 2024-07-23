from django.urls import resolve
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from apps.user.models import User
from common.code import USER_TYPE
from common.enum import E
from common.exception import EXCEPTION_CODE


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
                if request.user.username != view.kwargs.get('pk'):
                    raise PermissionDenied(code=EXCEPTION_CODE.NOT_PERMITTED_USER)
                else:
                    return True

        # 'update' 요청은 본인 또는 관리자만 가능
        if request.method in ['PUT', 'PATCH']:

            if request.user.role == str(USER_TYPE.ADMIN):
                return True
            elif request.user.role == str(USER_TYPE.USER):
                user_role = request.data.get('role')
                if user_role is not None:
                    return False
                else:
                    return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True


        return False


class AdminOrOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == str(USER_TYPE.ADMIN):
            return True
        elif request.user.role == str(USER_TYPE.USER):
            # 여기서 토큰값 체크하기
            return request.user.username == request.data.get('username')
        return False
