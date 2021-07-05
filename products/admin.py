from django.contrib import admin
from .models import Product, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'original_price', 'price', 'on_sale')
    list_filter = ('on_sale', 'category')
    search_fields = ('category', 'name')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_user', 'created')
    search_fields = ('user__first_name', 'user__last_name')

    def get_user(self, obj):
        return obj.user.full_name()
    get_user.short_description = 'User'


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
