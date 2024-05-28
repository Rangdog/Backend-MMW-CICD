from django.shortcuts import render

# Create your views here.
from django_rest_passwordreset.views import ResetPasswordRequestToken
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_rest_passwordreset.models import ResetPasswordToken
from .models import *
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


class CustomResetPasswordRequestToken(ResetPasswordRequestToken):
    serializer_class = CustomEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user_profile = Profile.objects.get(email=email)
        if user_profile:
            user = user_profile.user
            # Tạo token reset password
            token = ResetPasswordToken.objects.create(user=user)

            # Gửi email reset password (implement email sending here)
            # send_password_reset_email(email, token.key)
            sitelink = "http://localhost:5173/"
            full_link = str(sitelink)+str("password-reset/")+str(token)

            context = {
                'full_link': full_link,
                'email_address': email,
            }

            html_message = render_to_string(
                "backend/email.html", context=context)
            plain_message = strip_tags(html_message)

            msg = EmailMultiAlternatives(
                subject="Request for resetting password for {title}".format(
                    title=email),
                body=plain_message,
                from_email="thanhhaxuan02@gmail.com",
                to=[email]
            )
            msg.attach_alternative(html_message, "text/html")
            msg.send()

            return Response({'status': 'OK'})
        else:
            return Response({'status': 'Không tìm thấy email'})


class CustomResetPasswordConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'OK'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
