from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.core.mail import send_mail
from django.conf import settings
import jwt
from datetime import datetime, timedelta


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=200)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def email_user(self, subject, message, html_message):
        send_mail(
            subject,
            message,
            settings.SERVER_EMAIL,
            [self.email],
            html_message=html_message,
            fail_silently=False
        )

    def get_jwt(self, exp=None):
        payload = {'pk': self.pk, 'exp': datetime.now() + timedelta(seconds=exp)}
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token
