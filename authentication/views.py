from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import User
from smtplib import SMTPException
from django.template.loader import render_to_string
from django.db.transaction import atomic
from django.conf import settings


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
