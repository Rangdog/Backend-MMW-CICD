from django.db import models
from login.models import *


class Depot(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
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
    gender = models.BooleanField(null=True, blank=True)
    email = models.EmailField(unique=True, max_length=100)
    address = models.CharField(max_length=200)
    company = models.CharField(max_length=100, null=True, blank=True)
    taxcode = models.CharField(max_length=15, null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=200)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)

    def get_price(self):
        product_price = ProductPrice.objects.filter(
            product__id=self.id, pricelist=Pricelist.objects.last()
        ).first()
        return product_price.price if product_price else ""


class ProductDepot(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    depot = models.ForeignKey(Depot, on_delete=models.PROTECT)
    inventory = models.IntegerField()
    in_stock = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(inventory__gte=0), name="inventory_non_negative"
            )
        ]


class Pricelist(models.Model):
    applied_date = models.DateTimeField(auto_now_add=True)
    expired_date = models.DateTimeField()

    class Meta:
        ordering = ["expired_date"]


class ProductPrice(models.Model):
    pricelist = models.ForeignKey(Pricelist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = (("pricelist", "product"),)
        db_table = "ProductPrice"


class OrderForm(models.Model):
    partner = models.ForeignKey(BusinessPartner, on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    depot = models.ForeignKey(Depot, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=20, decimal_places=2)


class commom_infor_detail(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    quantity = models.IntegerField()

    class Meta:
        abstract = True


class OrderDetail(commom_infor_detail):
    form = models.ForeignKey(OrderForm, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = (("form", "product"),)
        db_table = "OrderDetail"

    def save(self, *args, **kwargs):
        self.id = f"{self.form_id}-{self.product_id}"
        super(OrderDetail, self).save(*args, **kwargs)


class ImportForm(models.Model):
    order = models.OneToOneField(OrderForm, on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=20, decimal_places=2)


class ImportDetail(commom_infor_detail):
    form = models.ForeignKey(ImportForm, on_delete=models.CASCADE)
    order_detail = models.OneToOneField(OrderDetail, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("form", "order_detail"),)
        db_table = "ImportDetail"

    def save(self, *args, **kwargs):
        self.id = f"{self.form_id}-{self.order_detail_id}"
        super(ImportDetail, self).save(*args, **kwargs)


class ExportForm(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    partner = models.ForeignKey(BusinessPartner, on_delete=models.PROTECT)
    depot = models.ForeignKey(Depot, on_delete=models.PROTECT)
    pricelist = models.ForeignKey(Pricelist, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=20, decimal_places=2)


class ExportDetail(commom_infor_detail):
    form = models.ForeignKey(ExportForm, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = (("form", "product"),)
        db_table = "ExportDetail"

    def save(self, *args, **kwargs):
        self.id = f"{self.form_id}-{self.product_id}"
        super(ExportDetail, self).save(*args, **kwargs)


class FormFactory:
    @staticmethod
    def create_form(form_type, **kwargs):
        if form_type == "order":
            return OrderForm.objects.create(**kwargs)
        elif form_type == "import":
            return ImportForm.objects.create(**kwargs)
        elif form_type == "export":
            return ExportForm.objects.create(**kwargs)
        else:
            raise ValueError("Invalid form type")
