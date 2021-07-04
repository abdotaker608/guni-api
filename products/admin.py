from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'original_price', 'price', 'on_sale')
    list_filter = ('on_sale', 'category')
    search_fields = ('category', 'name')


admin.site.register(Product, ProductAdmin)
