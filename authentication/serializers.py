from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializer(ModelSerializer):

    class Meta:
        fields = ['id', 'first_name', 'last_name', 'email', 'auth_token']
        model = User
