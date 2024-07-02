
import jwt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, CSRFCheck, TokenAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError

from apps.user.models import User, LoginSessions
from config import settings


# 유저와 토큰이 유효한지를 여기서 체크해야합니다.
class CommonJWTAuthenticate(TokenAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None

        try:
            prefix = authorization_header.split(' ')[0] # Baerer 자르기
            if prefix.lower() != 'bearer':
                raise print('Token is not Bearer jwt')

            access_token = authorization_header.split(' ')[1]
            user_token = LoginSessions.objects.filter(token=access_token).first()
            if user_token.token == access_token:
                payload = jwt.decode(
                    access_token, settings.SECRET_KEY, algorithms=['HS256']
                )
                custom_user = CustomUser(username=payload['username'], role=payload['role'])
        # 예외 처리하기
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return self.authenticate_credentials(custom_user)

    # key : username 값
    def authenticate_credentials(self, custom_user):
        if custom_user is None:
            raise AuthenticationFailed('User not found')

        return (custom_user, None)
class CustomUser:
    def __init__(self, username, role):
        self.username = username
        self.role = role
