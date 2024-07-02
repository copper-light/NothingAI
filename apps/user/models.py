from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

import common.code as c
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

# BaseUserManager 상속 받아서 사용자 모델의  manager 를 커스터마이징 할때는 create_user, create_superuser메서드를 정의해야한다.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        return self.create_user(
            email,
            password=password,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            **extra_fields,
        )
    # - User table model 기존 테이블 형태


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True) # 장고에서는 기본적으로 모델에는 id라는 이름의 자동 증가 필드가 포함되서 넣어줘야함
    name = models.CharField(max_length=50, default="Unknown")  # 사용자 이름
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, verbose_name="email address")
    description = models.TextField(default=False)
    password = models.CharField(max_length=255)

    role = models.CharField(max_length=10,  default=c.USER_TYPE.USER) # defult : admin (0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()  # 재정의 된 UserManager 사용 선언
    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ['username']# email을 ID 필드로 사용 선언 : vl

    def __str__(self):
        return self.email
    class Meta:
        app_label = "user"


class LoginSessions(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, db_column='user_id')
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
