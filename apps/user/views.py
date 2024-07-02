from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.utils.decorators import method_decorator
from rest_framework import filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken

from apps.user.models import LoginSessions, User
from common.authenticate import CommonJWTAuthenticate
from common.code import USER_TYPE
from common.pagination import CommonPagination
from common.permission import IsAuthorUpdateOrReadonly, AdminOrOwnerPermission
from common.response import ResponseBody
from common.swagger import list_resources, retrieve_resource
from common.viewsets import CommonViewSet
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from common.exception import EXCEPTION_CODE
from .serializers import UserLoginSerializer, UserSerializer
@method_decorator(name='list', decorator=list_resources)
@method_decorator(name='retrieve', decorator=retrieve_resource)
class UserViews(CommonViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'email')
    pagination_class = CommonPagination
    root_dir = settings.MODELS_DIR
    list_fields = ('id','username', 'role', 'email', 'created_at', 'updated_at') # 전체조회
    authentication_classes = [CommonJWTAuthenticate]
    # permission_classes = [IsAuthorUpdateOrReadonly]

    def check_path_user_match(self,review_author, pk):
        if pk != review_author.username:
            raise ValidationError(code=EXCEPTION_CODE.USER_NOT_FOUND_VALUE,  detail={pk: [pk]})
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthorUpdateOrReadonly]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        review_author = self.request.user
        self.check_path_user_match(review_author, kwargs.get('pk'))
        email = request.data.get('email')
        existing_user = User.objects.get(email=email)

        instance = User.objects.get(username=existing_user.username)
        if request.method == "PUT":
            partial = kwargs.pop('partial', False)
        else:
            partial = kwargs.pop('partial', True)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ResponseBody(detail=f"Successfully update", data=serializer.data, code=status.HTTP_200_OK).response()


    # 회원 상세 조회
    def retrieve(self, request, *args, **kwargs):
        # self : 클래스 자체 UserViews
        queryset = User.objects.filter(username=kwargs.get('pk'))
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
        return ResponseBody(detail=f"Successfully retrieve", data=serializer.data,code=status.HTTP_200_OK).response()

    # 회원 삭제
    def destroy(self, request, *args, **kwargs):
        username = request.data.get('username')
        review_author = self.request.user
        self.check_path_user_match(review_author, kwargs.get('pk'))
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return ValidationError(code=EXCEPTION_CODE.USER_NOT_FOUND_VALUE)
        except DatabaseError as e:
            raise ValidationError({'error': 'Database error occurred'}, code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user.is_active = False
        user.delete()

        return ResponseBody(detail="Successfully destroy!", code=status.HTTP_200_OK).response()



class UserLoginLogoutViewSet(CommonViewSet):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request: Request):

        username = request.data.get('username', None)
        password = request.data.get('password', None)
        # 사용자가 존재하는지 확인
        try:
            user = User.objects.get(username=username, password=password)
        except ObjectDoesNotExist as e:
            raise ValidationError(code=EXCEPTION_CODE.USER_NOT_FOUND_VALUE,  detail={username: [username]})

        login_sessions = LoginSessions.objects.filter(user=user)
        if login_sessions.exists():
            # 이미 로그인 세션이 존재하는 경우
            return ResponseBody(data=login_sessions.first().token, detail="Already login", code=status.HTTP_200_OK).response()
        else:
            # 로그인 세션 생성
            token = TokenObtainPairSerializer.get_token(user)
            token['username'] = user.username
            token['role'] = user.role
            token['created_at'] = str(user.created_at)
            access_token = str(token.access_token)
            login_session = LoginSessions(token=access_token, created_at=datetime.now(), user=user)
            login_session.save()
            return ResponseBody(data={"token":access_token}, detail="Successfully Login!", code=status.HTTP_200_OK).response()


    @action(detail=False, methods=['post'], url_path='logout', permission_classes=[AdminOrOwnerPermission])
    def logout(self, request: Request):

        review_author = self.request.user # 본인
        username = request.data.get('username', None)

        try:
            user = User.objects.get(username=username)
            logout_sessions = LoginSessions.objects.filter(user=user)
        except User.DoesNotExist:
            raise InvalidToken("User not found")

        if review_author.role == USER_TYPE.USER:
            if logout_sessions.exists() and f'Bearer {logout_sessions.first().token}' == request.META.get('HTTP_AUTHORIZATION'):
                logout_sessions.delete()
                return ResponseBody(code=status.HTTP_200_OK).response()
            else:
                raise ValidationError(code=EXCEPTION_CODE.INVALID_TOKEN,  detail={request.META.get('HTTP_AUTHORIZATION'): [request.META.get('HTTP_AUTHORIZATION')]})
        else:
            logout_sessions.delete()
            return ResponseBody(detail="Successfully Logout!", code=status.HTTP_200_OK).response()


