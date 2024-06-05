from django.db import models
from login.models import *
# Create your models here.


class Depot(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.BooleanField(null=True, blank=True)
    birthdate = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, max_length=100)


class BusinessPartner(models.Model):
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

    def get_price(self):
        product_price = ProductPrice.objects.filter(
            product__id=self.id, pricelist=Pricelist.objects.last()).first()
        return product_price.price if product_price else ""


class ProductDepot(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    inventory = models.IntegerField()
    in_stock = models.BooleanField(default=False)


class Pricelist(models.Model):
    applied_date = models.DateTimeField(auto_now_add=True)
    expired_date = models.DateTimeField(blank=True)

    class Meta:
        ordering = ['expired_date']


class ProductPrice(models.Model):
    pricelist = models.ForeignKey(Pricelist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)


class OrderForm(models.Model):
    partner = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=20, decimal_places=2)


class commom_infor_detail(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    quantity = models.IntegerField()

    class Meta:
        abstract = True


class OrderDetail(commom_infor_detail):
    form = models.ForeignKey(OrderForm, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = (('form', 'product'),)
        db_table = 'Order_Detail'

    def save(self, *args, **kwargs):
        self.id = f"{self.form_id}-{self.product_id}"
        super(OrderDetail, self).save(*args, **kwargs)


class ImportForm(models.Model):
    order = models.OneToOneField(
        OrderForm, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=20, decimal_places=2)


class ImportDetail(commom_infor_detail):
    form = models.ForeignKey(ImportForm, on_delete=models.CASCADE)
    order_detail = models.OneToOneField(OrderDetail, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('form', 'order_detail'),)
        db_table = 'Import_Detail'

    def save(self, *args, **kwargs):
        self.id = f"{self.form_id}-{self.order_detail_id}"
        super(ImportDetail, self).save(*args, **kwargs)


class ExportForm(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    partner = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE)
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    pricelist = models.ForeignKey(Pricelist, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=20, decimal_places=2)


class ExportDetail(commom_infor_detail):
    form = models.ForeignKey(ExportForm, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = (('form', 'product'),)
        db_table = 'Export_Detail'

    def save(self, *args, **kwargs):
        self.id = f"{self.form_id}-{self.product_id}"
        super(ExportDetail, self).save(*args, **kwargs)
