from rest_framework import generics, mixins, status
from .models import Product, PurchasedProduct, Order
from .serializers import ProductSerializer, OrderSerializer
from .filters import AdvancedProductsFilter
from .pagination import SimplePaginator
from authentication.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
import stripe


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


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_payment_intent(request):
    stripe.api_key = settings.STRIPE_API_SECRET
    data = request.data
    total_price = int(float(data['total_price']) * 100)
    payment_intent = stripe.PaymentIntent.create(
        amount=total_price,
        currency='USD'
    )
    return Response({'clientSecret': payment_intent['client_secret']}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_order(request):
    data = request.data
    intent_id = data['intent_id']
    intent = stripe.PaymentIntent.retrieve(intent_id)
    if intent.status != 'succeeded':
        return Response({'status': 400}, status=status.HTTP_400_BAD_REQUEST)
    user_id = data['user_id']
    user = User.objects.get(id=user_id)
    items = data['items']
    total_price = data['total_price']
    order = Order.objects.create(user=user, intent_id=intent_id, total_price=total_price)
    for item in items:
        item.pop('id')
        purchased_product = PurchasedProduct.manager.create(**item)
        order.products.add(purchased_product)
    serializer = OrderSerializer(order)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
