from django.shortcuts import render

# Create your views here.
from django_rest_passwordreset.views import ResetPasswordRequestToken
from .serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import action
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
from django.db.transaction import atomic, set_rollback
from datetime import datetime


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

    @atomic
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
        is_active = bool(data.get('is_active', False))
        is_superuser = bool(data.get('is_active', False))
        depot_user = request.user.profile.depot
        try:
            profile = Profile.objects.create(user=None, depot=depot_user, first_name=first_name, last_name=last_name,
                                             email=email, phone=phone, birthdate=birthdate, address=address, gender=gender)
            custom_user = CustomUser.objects.create(username=first_name+last_name + "_" + str(profile.id),
                                                    password=first_name + last_name, is_active=is_active, is_superuser=is_superuser)
        except Exception as e:
            set_rollback(True)
            return Response({"lỗi": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        profile.user = custom_user
        profile.save()
        return Response(status=status.HTTP_201_CREATED)

    @atomic
    def update(self, request, *args, **kwargs):
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
        is_active = bool(data.get('is_active', False))
        is_superuser = bool(data.get('is_active', False))
        pk = kwargs.get('pk')
        profile = Profile.objects.filter(pk=pk).first()
        user = profile.user
        try:
            profile.first_name = first_name
            profile.last_name = last_name
            profile.gender = gender
            profile.birthdate = birthdate
            profile.address = address
            profile.phone = phone
            user.is_active = is_active
            user.is_superuser = is_superuser
            profile.save()
            user.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            set_rollback(True)
            return Response({"lỗi": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class BusinessPartnerviewset(viewsets.ModelViewSet):
    queryset = BusinessPartner.objects.all()
    serializer_class = BusinessPartnerSerializer


class Categoryviewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class Productviewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name', "")
        unit = data.get('unit', "")
        category = data.get('category', None)
        inventory = data.get('inventory', 0)
        if isinstance(category, str):
            try:
                tmp_category = Category.objects.create(name=category)
                product = Product.objects.create(
                    category=tmp_category, name=name, unit=unit)
                ProductDepot.objects.create(
                    product=product, inventory=inventory, depot=request.user.profile.depot)
                return Response("Thành công", status=status.HTTP_201_CREATED)
            except Exception as e:
                set_rollback(True)
                return Response({"lỗi": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                tmp_category = Category.objects.get(pk=category.get('id'))
                product = Product.objects.create(
                    category=tmp_category, name=name, unit=unit)
                ProductDepot.objects.create(
                    product=product, inventory=inventory, depot=request.user.profile.depot)
                return Response("Thành công", status=status.HTTP_201_CREATED)
            except Exception as e:
                set_rollback(True)
                return Response({"lỗi": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @atomic
    def update(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name', "")
        unit = data.get('unit', "")
        category = data.get('category', None)
        pk = kwargs.get('pk')
        product = Product.objects.get(pk=pk)
        if isinstance(category, str):
            try:
                tmp_category = Category.objects.create(name=category)
                product.category = tmp_category
                product.name = name
                product.unit = unit
                product.save()
                return Response("Thành công", status=status.HTTP_201_CREATED)
            except Exception as e:
                set_rollback(True)
                return Response({"lỗi": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                tmp_category = Category.objects.get(pk=category.get('id'))
                product.category = tmp_category
                product.name = name
                product.unit = unit
                product.save()
                return Response("Thành công", status=status.HTTP_201_CREATED)
            except Exception as e:
                set_rollback(True)
                return Response({"lỗi": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


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
    # @action(methods=['post'], url_path='filter_detail')
    # def create_or_update:

    @atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        created_date = data.get('created_date', None)
        if created_date:
            try:
                created_date = datetime.strptime(
                    created_date, '%d/%m/%Y')
                # Assuming 'YourModel' has a 'created_date' DateTimeField
            except ValueError as e:
                return Response(f"Error parsing date: {e}", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("No date provided", status=status.HTTP_400_BAD_REQUEST)
        depot = data.get('depot', None)
        details = data.get('details', None)
        partner = data.get('partner', None)
        total = data.get('total', None)
        try:
            tmp_partner = BusinessPartner.objects.get(pk=partner.get('id'))
            tmp_depot = Depot.objects.get(pk=depot.get('id'))
            order_form = OrderForm.objects.create(partner=tmp_partner, user=request.user,
                                                  depot=tmp_depot, created_date=created_date, total=total)
            for orderdetail in details:
                tmp_product = Product.objects.get(
                    pk=int((orderdetail.get('product')).get('id')))

                OrderDetail.objects.create(form=order_form, product=tmp_product, price=float(orderdetail.get(
                    'price')), quantity=int(orderdetail.get('quantity')))
            return Response("Thành công", status=status.HTTP_200_OK)
        except Exception as e:
            set_rollback(True)
            return Response({"lỗi": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @atomic
    def update(self, request, *args, **kwargs):
        data = request.data
        depot = data.get("depot", None)
        details = data.get("details", None)
        partner = data.get("partner", None)
        total = data.get("total", None)
        pk = kwargs.get("pk")
        try:
            tmp_partner = BusinessPartner.objects.get(pk=partner.get("id"))
            tmp_depot = Depot.objects.get(pk=depot.get("id"))
            OrderForm.objects.filter(pk=pk).update(
                partner=tmp_partner,
                user=request.user,
                depot=tmp_depot,
                total=total,
            )
            order_form = OrderForm.objects.get(pk=pk)
            orderdetails = OrderDetail.objects.filter(form=order_form)
            # CREATE NEW DETAIL OR UPDATE OLD DETAIL.
            for detail in details:
                for orderdetail in orderdetails:
                    if orderdetail.id == detail["id"]:
                        orderdetail.quantity = detail["quantity"]
                        orderdetail.price = detail["price"]
                        orderdetail.save()
                        break
                else:
                    tmp_product = Product.objects.get(
                        pk=detail["product"]["id"])
                    OrderDetail.objects.create(
                        form=order_form,
                        product=tmp_product,
                        quantity=detail["quantity"],
                        price=detail["price"],
                    )
            # DELETE DETAIL.
            deleted_details = []
            for orderdetail in orderdetails:
                for detail in details:
                    if detail["id"] == orderdetail.id:
                        break
                else:
                    deleted_details.append(orderdetail)
            else:
                for detail in deleted_details:
                    detail.delete()
            return Response("Thành công", status=status.HTTP_200_OK)
        except Exception as e:
            set_rollback(True)
            print(e)
            return Response({"lỗi": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailviewset(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer

    @ action(methods=['get'], detail=True, url_path='filter_detail')
    def filter_detail(self, request, pk=None):
        order_details = OrderDetail.objects.filter(form__id=pk)
        serializer = OrderDetailSerializer(order_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImportFormviewset(viewsets.ModelViewSet):
    queryset = ImportForm.objects.all()
    serializer_class = ImportFormSerializer


class ImportDetailviewset(viewsets.ModelViewSet):
    queryset = ImportDetail.objects.all()
    serializer_class = ImportDetailSerializer

    @ action(methods=['get'], detail=True)
    def filter_detail(self, request, pk: int):
        importDetail = ImportDetail.objects.filter(form__id=pk)
        if importDetail.exists():
            serializer = ImportDetailSerializer(importDetail, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Not found.'}, status=status.HTTP_400_BAD_REQUEST)


class ExportFormviewset(viewsets.ModelViewSet):
    queryset = ExportForm.objects.all()
    serializer_class = ExportFormSerializer

    @atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        created_date = data.get('created_date', None)
        if created_date:
            try:
                created_date = datetime.strptime(
                    created_date, '%d/%m/%Y')
                # Assuming 'YourModel' has a 'created_date' DateTimeField
            except ValueError as e:
                return Response(f"Error parsing date: {e}", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("No date provided", status=status.HTTP_400_BAD_REQUEST)
        depot = data.get('depot', None)
        details = data.get('details', None)
        partner = data.get('partner', None)
        total = data.get('total', None)
        try:
            tmp_partner = BusinessPartner.objects.get(pk=partner.get('id'))
            tmp_depot = Depot.objects.get(pk=depot.get('id'))
            export_form = ExportForm.objects.create(partner=tmp_partner, user=request.user,
                                                    depot=tmp_depot, created_date=created_date, total=total, pricelist=Pricelist.objects.last())
            for exportdetail in details:
                tmp_product = Product.objects.get(
                    pk=int((exportdetail.get('product')).get('id')))

                ExportDetail.objects.create(form=export_form, product=tmp_product, price=float(exportdetail.get(
                    'price')), quantity=int(exportdetail.get('quantity')))
            return Response("Thành công", status=status.HTTP_200_OK)
        except Exception as e:
            set_rollback(True)
            return Response({"lỗi": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @ atomic
    def update(self, request, *args, **kwargs):
        data = request.data
        created_date = data.get('created_date', None)
        if created_date:
            try:
                created_date = datetime.strptime(
                    created_date, '%d/%m/%Y')
                # Assuming 'YourModel' has a 'created_date' DateTimeField
            except ValueError as e:
                return Response(f"Error parsing date: {e}", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("No date provided", status=status.HTTP_400_BAD_REQUEST)
        depot = data.get('depot', None)
        details = data.get('details', None)
        partner = data.get('partner', None)
        total = data.get('total', None)
        pk = kwargs.get('pk')
        try:
            tmp_partner = BusinessPartner.objects.get(pk=partner.get('id'))
            tmp_depot = Depot.objects.get(pk=depot.get('id'))
            ExportForm.objects.filter(pk=pk).update(partner=tmp_partner, user=request.user,
                                                    depot=tmp_depot, created_date=created_date, total=total)
            export_form = ExportForm.objects.get(pk=pk)
            exportdetails = ExportDetail.objects.filter(form=export_form)
            if exportdetails.exists():
                for exportdetail in details:
                    tmp_product = Product.objects.get(
                        pk=int((exportdetail.get('product')).get('id')))
                    tmp_exportdetail = ExportDetail.objects.get(
                        pk=exportdetail.get('id'))
                    tmp_exportdetail.form = export_form
                    tmp_exportdetail.product = tmp_product
                    tmp_exportdetail.price = float(exportdetail.get(
                        'price'))
                    tmp_exportdetail.quantity = int(
                        exportdetail.get('quantity'))
                    tmp_exportdetail.save()
                    exportdetails = exportdetails.exclude(
                        pk=exportdetail.get('id'))
                exportdetails.delete()
                return Response("Thành công", status=status.HTTP_200_OK)
            else:
                for exportdetail in details:
                    tmp_product = Product.objects.get(
                        pk=int((exportdetail.get('product')).get('id')))

                    ExportDetail.objects.create(form=export_form, product=tmp_product, price=float(exportdetail.get(
                        'price')), quantity=int(exportdetail.get('quantity')))
                return Response("Thành công", status=status.HTTP_200_OK)
        except Exception as e:
            set_rollback(True)
            return Response({"lỗi": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class ExportDetailviewset(viewsets.ModelViewSet):
    queryset = ExportDetail.objects.all()
    serializer_class = ExportDetailSerializer

    @ action(methods=['get'], detail=True)
    def filter_detail(self, request, pk: int):
        exportDetail = ExportDetail.objects.filter(form__id=pk)
        if exportDetail.exists():
            serializer = ExportDetailSerializer(exportDetail, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Not found.'}, status=status.HTTP_400_BAD_REQUEST)
