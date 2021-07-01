from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductView.as_view(), name='product'),
    path('f', views.ProductFilterView.as_view(), name='product_filter')
]
