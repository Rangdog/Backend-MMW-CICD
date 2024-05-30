from django.db import models
from login.models import *
# Create your models here.


class Depot(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.BooleanField(null=True, blank=True)
    birthdate = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, max_length=100)


class Business_Partner(models.Model):
    name = models.CharField(max_length=100)
    gender = models.BooleanField(null=True)
    email = models.EmailField(unique=True, max_length=100)
    address = models.CharField(max_length=200)
    company = models.CharField(max_length=100, null=True, blank=True)
    taxcode = models.CharField(max_length=15, null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=200)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)


class Product_Depot(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    inventory = models.IntegerField()


class Pricelist(models.Model):
    applied_date = models.DateTimeField(auto_now_add=True)
    expired_date = models.DateTimeField()


class Product_Price(models.Model):
    pricelist = models.ForeignKey(Pricelist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)


class Order_Form(models.Model):
    partner = models.ForeignKey(Business_Partner, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=20, decimal_places=2)


class Order_Detail(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    order = models.ForeignKey(Order_Form, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = (('order', 'product'),)
        db_table = 'Order_Detail'

    def save(self, *args, **kwargs):
        self.id = f"{self.order_id}-{self.product_id}"
        super(Order_Detail, self).save(*args, **kwargs)


class Import_Form(models.Model):
    order = models.OneToOneField(Order_Form, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=20, decimal_places=2)


class Import_Detail(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    id_import = models.ForeignKey(Import_Form, on_delete=models.CASCADE)
    order_detail = models.OneToOneField(Order_Detail, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = (('id_import', 'order_detail'),)
        db_table = 'Import_Detail'

    def save(self, *args, **kwargs):
        self.id = f"{self.id_import_id}-{self.order_detail_id}"
        super(Order_Detail, self).save(*args, **kwargs)


class Export_Form(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    partner = models.ForeignKey(Business_Partner, on_delete=models.CASCADE)
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    pricelist = models.ForeignKey(Pricelist, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=20, decimal_places=2)


class Export_Detail(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    export = models.ForeignKey(Export_Form, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = (('export', 'product'),)
        db_table = 'Export_Detail'

    def save(self, *args, **kwargs):
        self.id = f"{self.export_id}-{self.product_id}"
        super(Order_Detail, self).save(*args, **kwargs)
