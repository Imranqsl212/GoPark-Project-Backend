from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        user = self.model(username=username, email=email, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")
        user = self.create_user(username, email, password, **extra_fields)
        setattr(user, "is_staff", True)

        return user


class MyUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=50,
        verbose_name="Имя пользователя",
        unique=True,
    )
    created_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    otp_code = models.CharField(
        max_length=6, blank=True, null=True, verbose_name="OTP Code"
    )

    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def str(self):
        return self.username
