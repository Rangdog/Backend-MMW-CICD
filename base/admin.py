from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Depot)
admin.site.register(Business_Partner)
admin.site.register(Category)
admin.site.register(Product_Depot)
admin.site.register(Pricelist)
admin.site.register(Product_Price)
admin.site.register(Order_Form)
admin.site.register(Order_Detail)
admin.site.register(Import_Form)
admin.site.register(Import_Detail)
admin.site.register(Export_Form)
admin.site.register(Export_Detail)
