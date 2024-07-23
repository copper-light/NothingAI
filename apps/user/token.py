# 파일 분리해서 토큰 클래스 생성 -> create_token() 넣기


from datetime import datetime

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.user.models import LoginSessions


def create_token(user):
    token = TokenObtainPairSerializer.get_token(user)
    token['username'] = user.username
    token['role'] = user.role
    token['created_at'] = str(user.created_at)
    access_token = str(token.access_token)
    login_session = LoginSessions(token=access_token, created_at=datetime.now(), user=user)
    login_session.save()

    return access_token

