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
from django.core.validators import validate_email
from django.utils.html import strip_tags
from django.db import transaction


class CustomResetPasswordRequestToken(ResetPasswordRequestToken):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = CustomEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user_profile = Profile.objects.get(email=email)
        if user_profile.user.username == username:
            user = user_profile.user
            # Tạo token reset password
            token = ResetPasswordToken.objects.create(user=user)
            # Gửi email reset password (implement email sending here)
            # send_password_reset_email(email, token.key)
            sitelink = "http://localhost:5173/"
            full_link = str(sitelink)+str("password-reset/")+str(token.key)

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
            return Response({'status': 'Lỗi, Vui lòng kiểm tra lại user và email'}, status=status.HTTP_400_BAD_REQUEST)


class CustomResetPasswordConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = CustomResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'status': 'OK'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplacePassword(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CustomRepalcePasswordConfirmSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Sai mật khẩu cũ"]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"status": "ok"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Depotviewset(viewsets.ModelViewSet):
    queryset = Depot.objects.all()
    serializer_class = DepotSerializer


class Profileviewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        first_name = data.get('first_name', "")
        last_name = data.get('last_name', "")
        gender = bool(data.get('gender', False))
        birthdate = data.get('birthdate', "")
        address = data.get('address', '')
        email = data.get('email', '')
        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)
        phone = data.get('phone', '')
        is_active = data.get('is_active', False)
        is_superuser = data.get('is_superuser', False)
        depot_user = Profile.objects.filter(user=request.user).first().depot
        try:
            with transaction.atomic():
                profile = Profile.objects.create(user=None, depot=depot_user, first_name=first_name, last_name=last_name,
                                                 email=email, phone=phone, birthdate=birthdate, address=address, gender=gender)
                custom_user = CustomUser.objects.create(username=first_name+last_name + "_" + str(profile.id),
                                                        password=first_name + last_name, is_active=is_active, is_superuser=is_superuser)
        except Exception as e:
            return Response({"lỗi": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        profile.user = custom_user
        profile.save()
        return Response(status=status.HTTP_201_CREATED)


class BusinessPartnerviewset(viewsets.ModelViewSet):
    queryset = BusinessPartner.objects.all()
    serializer_class = BusinessPartnerSerializer


class Categoryviewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class Productviewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDepotviewset(viewsets.ModelViewSet):
    queryset = ProductDepot.objects.all()
    serializer_class = ProductDepotSerializer


class Pricelistviewset(viewsets.ModelViewSet):
    queryset = Pricelist.objects.all()
    serializer_class = PricelistSerializer


class ProductPriceviewset(viewsets.ModelViewSet):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer


class OrderFormviewset(viewsets.ModelViewSet):
    queryset = OrderForm.objects.all()
    serializer_class = OrderFormSerializer


class OrderDetailviewset(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer


class ImportFormviewset(viewsets.ModelViewSet):
    queryset = ImportForm.objects.all()
    serializer_class = ImportFormSerializer


class ImportDetailviewset(viewsets.ModelViewSet):
    queryset = ImportDetail.objects.all()
    serializer_class = ImportDetailSerializer


class Export_Form_viewset(viewsets.ModelViewSet):
    queryset = ExportForm.objects.all()
    serializer_class = ExportFormSerializer


class Export_Detail_viewset(viewsets.ModelViewSet):
    queryset = ExportDetail.objects.all()
    serializer_class = ExportDetailSerializer
