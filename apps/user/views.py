
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from rest_framework import filters
from rest_framework.permissions import AllowAny
from apps.user.models import LoginSessions, User
from common.authenticate import CommonJWTAuthenticate, ListRetrieveJWTAuthenticate
from common.code import USER_TYPE
from common.pagination import CommonPagination
from common.permission import IsAuthorUpdateOrReadonly, AdminOrOwnerPermission
from common.response import ResponseBody
from common.swagger import list_resources, retrieve_resource
from common.viewsets import CommonViewSet
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from common.exception import EXCEPTION_CODE
from .serializers import UserSerializer, LoginSessionsSerializer
from .token import create_token


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
    authentication_classes = [CommonJWTAuthenticate, ListRetrieveJWTAuthenticate]
    # permission_classes = [IsAuthorUpdateOrReadonly]

    def check_path_user_match(self,username, pk):
        if pk != username.username:
            raise ValidationError(code=EXCEPTION_CODE.USER_NOT_FOUND_VALUE,  detail={pk: [pk]})
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthorUpdateOrReadonly]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        review_author = self.request.user
        # self.check_path_user_match(review_author, kwargs.get('pk'))
        #  db 에 입력한 데이터가 존재 하는 경우 이미 존재하는 이메일이라고 수정하지 못한다는 에러를 나타내야함.
        email = request.data.get('email')
        if email is not None:
            if User.objects.filter(email=email).exists():
                raise ValidationError(code=EXCEPTION_CODE.VALUE_EXISTS, detail={'email': [email]})

        instance = User.objects.get(username=kwargs.get('pk'))
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
        username_pk = kwargs.get('pk')
        queryset = User.objects.filter(username=username_pk)
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
        else:
            raise ValidationError(code=EXCEPTION_CODE.USER_NOT_FOUND_VALUE,  detail={username_pk: [username_pk]})
        return ResponseBody(detail=f"Successfully retrieve", data=serializer.data[0], code=status.HTTP_200_OK).response()

    # 회원 삭제
    def destroy(self, request, *args, **kwargs):
        # username = request.data.get('username')
        username_pk = kwargs.get('pk')
        # self.check_path_user_match(username, username_pk)
        try:
            user = User.objects.get(username=username_pk)
        except ObjectDoesNotExist:
            raise ValidationError(code=EXCEPTION_CODE.USER_NOT_FOUND_VALUE,  detail={username_pk: [username_pk]})

        user.is_active = False
        user.delete()
        return ResponseBody(detail="Successfully destroy!", code=status.HTTP_200_OK).response()

class UserLoginLogoutViewSet(CommonViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSessionsSerializer
    authentication_classes = [CommonJWTAuthenticate]
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request: Request):
        print("self result : ", self)
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        # 사용자가 존재하는지 확인
        try:
            user = User.objects.get(username=username, password=password)
        except ObjectDoesNotExist as e:
            raise ValidationError(code=EXCEPTION_CODE.USER_NOT_FOUND_VALUE,  detail={username: [username]})

        return ResponseBody(data={"token":create_token(user)}, code=status.HTTP_200_OK).response()


    @action(detail=False, methods=['post'], url_path='logout', permission_classes=[AdminOrOwnerPermission])
    def logout(self, request: Request):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
        except:
            raise ValidationError(code=EXCEPTION_CODE.USER_NOT_FOUND_VALUE,  detail={username: [username]})

        logout_sessions = LoginSessions.objects.filter(user=user).first()
        if logout_sessions is None:
            raise ValidationError(code=EXCEPTION_CODE.USER_NOT_FOUND_VALUE,  detail={username: [username]})

        prefix = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        session_user = LoginSessions.objects.filter(token=prefix).first()

        head_token_user = User.objects.filter(id=session_user.user_id).first()
        user_role = request.user.role if hasattr(request.user, 'role') else 'Unknown'
        if user_role == '1':
            if head_token_user.username == request.data.get('username') and prefix == logout_sessions.token:
                logout_sessions.delete()
                return ResponseBody(code=status.HTTP_200_OK).response()
            else :
                raise ValidationError(code=EXCEPTION_CODE.USER_NOT_FOUND_VALUE, detail={username: [username]})
        else:
            logout_sessions.delete()
            return ResponseBody(code=status.HTTP_200_OK).response()
