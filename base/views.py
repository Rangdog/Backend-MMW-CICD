from django.shortcuts import render

# Create your views here.
from django_rest_passwordreset.views import ResetPasswordRequestToken
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from knox.auth import TokenAuthentication
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


# class DepotMixinView(mixins.ListModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
#     # security
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAuthenticated]
#     queryset = Depot.objects.all()
#     serializer_class = DepotSerializer
#     lookup_field = 'pk'

#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         if pk is not None:
#             return self.retrieve(request, *args, **kwargs)
#         return self.list(request, *args, **kwargs)

class Depot_viewset(viewsets.ModelViewSet):
    queryset = Depot.objects.all()
    serializer_class = Depot_Serializer


class Profile_viewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = Profile_Serializer


class Business_Partner_viewset(viewsets.ModelViewSet):
    queryset = Business_Partner.objects.all()
    serializer_class = Business_Partner_Serializer


class Category_viewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = Category_Serializer


class Product_viewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = Product_Serializer


class Product_Depot_viewset(viewsets.ModelViewSet):
    queryset = Product_Depot.objects.all()
    serializer_class = Product_Depot_Serializer


class Pricelist_viewset(viewsets.ModelViewSet):
    queryset = Pricelist.objects.all()
    serializer_class = Pricelist_Serializer


class Product_Price_viewset(viewsets.ModelViewSet):
    queryset = Product_Price.objects.all()
    serializer_class = Product_Price_Serializer


class Order_Form_viewset(viewsets.ModelViewSet):
    queryset = Order_Form.objects.all()
    serializer_class = Order_Form_Serializer


class Order_Detail_viewset(viewsets.ModelViewSet):
    queryset = Order_Detail.objects.all()
    serializer_class = Order_Detail_Serializer


class Import_Form_viewset(viewsets.ModelViewSet):
    queryset = Import_Form.objects.all()
    serializer_class = Import_Form_Serializer


class Import_Detail_viewset(viewsets.ModelViewSet):
    queryset = Import_Detail.objects.all()
    serializer_class = Import_Detail_Serializer


class Export_Form_viewset(viewsets.ModelViewSet):
    queryset = Export_Form.objects.all()
    serializer_class = Export_Form_Serializer


class Export_Detail_viewset(viewsets.ModelViewSet):
    queryset = Export_Detail.objects.all()
    serializer_class = Export_Detail_Serializer
