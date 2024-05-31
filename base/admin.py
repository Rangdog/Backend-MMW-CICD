from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Depot)
admin.site.register(BusinessPartner)
admin.site.register(Category)
admin.site.register(ProductDepot)
admin.site.register(Pricelist)
admin.site.register(ProductPrice)
admin.site.register(OrderForm)
admin.site.register(OrderDetail)
admin.site.register(ImportForm)
admin.site.register(ImportDetail)
admin.site.register(ExportForm)
admin.site.register(ExportDetail)
