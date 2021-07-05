from .models import Product, Order
from rest_framework.serializers import ModelSerializer


class ProductSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Product


class OrderSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Order