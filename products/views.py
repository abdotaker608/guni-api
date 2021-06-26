from rest_framework import generics, mixins, status
from .models import Product
from .serializers import ProductSerializer


class ProductView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProductSerializer

    def get(self, request):
        return self.list(request)

    def get_queryset(self):
        hot_flag = self.request.query_params.get('hot', False)

        if hot_flag:
            return Product.manager.hot_items()
