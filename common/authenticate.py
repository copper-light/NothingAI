
import jwt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, CSRFCheck, TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError

from apps.user.models import User, LoginSessions
from common.exception import EXCEPTION_CODE
from config import settings


# 유저와 토큰이 유효한지를 여기서 체크해야합니다.
class CommonJWTAuthenticate(TokenAuthentication):
    def authenticate(self, request):
        # 특정 action -> action  -> super (authenticate())
        # 허용 x -> raise

        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None

        prefix = authorization_header.split(' ')[0] # Baerer 자르기
        if prefix.lower() != 'bearer':
            raise print('Token is not Bearer jwt')

        access_token = authorization_header.split(' ')[1]
        user_token = LoginSessions.objects.filter(token=access_token).first()
        if not user_token:
            raise InvalidToken(code=EXCEPTION_CODE.INVALID_TOKEN, detail={'Token':['Token']}) # 인증되지 않은 사용자.

        if user_token.token == access_token:
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256']
            )
            custom_user = CustomUser(username=payload['username'], role=payload['role'])
            return self.authenticate_credentials(custom_user)

    # key : username 값
    def authenticate_credentials(self, custom_user):
        if custom_user is None:
            raise InvalidToken(code=EXCEPTION_CODE.INVALID_TOKEN, detail={'Token':['Token']})

        return (custom_user, None)
class CustomUser:
    def __init__(self, username, role):
        self.username = username
        self.role = role


class ListRetrieveJWTAuthenticate(CommonJWTAuthenticate):
    def authenticate(self, request):
        if request.method in ['GET']:
            authorization_header = request.headers.get('Authorization')
            if not authorization_header:
                raise ValidationError(code=EXCEPTION_CODE.NOT_EXISTS_TOKEN, detail={'Token': ['Token']})

            return super().authenticate(request)

        raise InvalidToken(code=EXCEPTION_CODE.INVALID_TOKEN, detail={'Token': ['Token']})  # 인증되지 않은 사용자.