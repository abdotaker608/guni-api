from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import User
from smtplib import SMTPException
from django.template.loader import render_to_string
from django.db.transaction import atomic
from django.conf import settings
import jwt
from django.db.models import ObjectDoesNotExist
from .serializers import UserSerializer


@api_view(['POST'])
def register_user(request):
    try:
        with atomic():
            data = request.data
            if User.objects.filter(email=data['email']).exists():
                return Response({"status": 400, "error": {
                    "message": "This email is already taken!"
                }}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(**data)
            verify_link = f"{settings.FRONT_END_HOST}/verify?token={user.get_jwt(60 * 60 * 24 * 3)}"
            html_string = render_to_string('registration.html', {'link': verify_link})
            user.email_user(
                'Email Address Verification',
                'Please verify your email address to complete your signup!',
                html_string
            )
            return Response({"status": 200, "success": True}, status=status.HTTP_200_OK)
    except SMTPException:
        return Response({"status": 503}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
def verify_user(request):
    token = request.data.get('token')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        try:
            user = User.objects.get(pk=payload['pk'])
            if user.is_active:
                return Response({"status": 400, "error": {
                    "message": "Your email is already verified!"
                }}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            user.save()
            serializer = UserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"status": 400, "error": {
                "message": "Invalid token!"
            }}, status=status.HTTP_400_BAD_REQUEST)

    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return Response({"status": 400, "error": {
            "message": "Invalid or expired token!"
        }}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def verify_token(request):
    authorization = request.headers['authorization']
    token = authorization.split(' ')[1]
    try:
        user = User.objects.get(auth_token=token)
        if not user.is_active:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def login_user(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    try:
        user = User.objects.get(email=email)
        if not user.is_active:
            return Response({"status": 401, "error": {
                "message": "You need to activate your account before you can login!"
            }}, status=status.HTTP_401_UNAUTHORIZED)
        if user.check_password(password):
            serializer = UserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"status": 401, "error": {
                "message": "This combination of email and password is not recognized."
            }}, status=status.HTTP_401_UNAUTHORIZED)
    except ObjectDoesNotExist:
        return Response({"status": 401, "error": {
            "message": "This combination of email and password is not recognized."
        }}, status=status.HTTP_401_UNAUTHORIZED)