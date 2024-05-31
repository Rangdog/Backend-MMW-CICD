from django_rest_passwordreset.serializers import EmailSerializer
from django_rest_passwordreset.models import ResetPasswordToken
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError


class CustomEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not Profile.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email không tồn tại')
        return value


class CustomResetPasswordConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get('token')
        password = attrs.get('password')

        try:
            reset_password_token = ResetPasswordToken.objects.get(key=token)
        except ResetPasswordToken.DoesNotExist:
            raise ValidationError('Token không hợp lệ')

        user = reset_password_token.user
        if not user.is_active:
            raise ValidationError('Tài khoản không hoạt động')

        # Đặt lại mật khẩu cho người dùng
        user.set_password(password)
        user.save()

        # Xóa tất cả các token password reset của người dùng
        ResetPasswordToken.objects.filter(user=user).delete()

        return attrs


class Depot_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Depot
        fields = '__all__'


class Profile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class Business_Partner_Serializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartner
        fields = '__all__'


class Category_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class Product_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class Product_Depot_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDepot
        fields = '__all__'


class Pricelist_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Pricelist
        fields = '__all__'


class Product_Price_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = '__all__'


class Order_Form_Serializer(serializers.ModelSerializer):
    class Meta:
        model = OrderForm
        fields = '__all__'


class Order_Detail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'


class Import_Form_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ImportForm
        fields = '__all__'


class Import_Detail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ImportDetail
        fields = '__all__'


class Export_Form_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ExportForm
        fields = '__all__'


class Export_Detail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ExportDetail
        fields = '__all__'
