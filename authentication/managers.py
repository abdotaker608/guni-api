from django.contrib.auth.base_user import BaseUserManager
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra):
        user = self.model.objects.create(email=email, **extra)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user

    def create_user(self, email, password, **extra):
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        extra.setdefault('is_active', True)
        return self._create_user(email, password, **extra)
