from rest_framework import generics, mixins, status
from .models import Product
from .serializers import ProductSerializer
from .filters import AdvancedProductsFilter
from .pagination import SimplePaginator


class ProductView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProductSerializer

    def get(self, request):
        return self.list(request)

    def get_queryset(self):
        hot_flag = self.request.query_params.get('hot', False)

        if hot_flag:
            return Product.manager.hot_items()


class ProductFilterView(generics.GenericAPIView, mixins.ListModelMixin):

    queryset = Product.manager.all()
    serializer_class = ProductSerializer
    filter_backends = [AdvancedProductsFilter]
    pagination_class = SimplePaginator
    pagination_class.page_size = 5
    ordering = ('-created', )

    def get(self, request):
        return self.list(request)
