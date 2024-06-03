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
        username = serializer.validated_data['username']
        user_profile = Profile.objects.get(email=email)
        if user_profile.user.username == username:
            user = user_profile.user
            # Tạo token reset password
            token = ResetPasswordToken.objects.create(user=user)
            print(token.key)
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

    def post(self, request, *args, **kwargs):
        serializer = CustomResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
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

class Depotviewset(viewsets.ModelViewSet):
    queryset = Depot.objects.all()
    serializer_class = DepotSerializer


class Profileviewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


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
