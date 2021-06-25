from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):

    list_display = ('full_name', 'email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')

    @staticmethod
    def full_name(obj):
        return obj.full_name()


admin.site.register(User, UserAdmin)
