from .models import Product
from rest_framework.serializers import ModelSerializer


class ProductSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Product
