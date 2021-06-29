from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('register', views.register_user, name='register'),
    path('verify', views.verify_user, name='verify'),
    path('token/verify', views.verify_token, name='verify_token'),
    path('login', views.login_user, name='login')
]