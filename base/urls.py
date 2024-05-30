from django.urls import path, include

from . import views
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register(r'depot', Depot_viewset)
router.register(r'profile', Profile_viewset)
router.register(r'business_Partner', Business_Partner_viewset)
router.register(r'category', Category_viewset)
router.register(r'product', Product_viewset)
router.register(r'product_depot', Product_Depot_viewset)
router.register(r'pricelist', Pricelist_viewset)
router.register(r'product_price', Product_Price_viewset)
router.register(r'order_form', Order_Form_viewset)
router.register(r'order_detail', Order_Detail_viewset)
router.register(r'import_form', Import_Form_viewset)
router.register(r'import_detail', Import_Detail_viewset)
router.register(r'export_form', Export_Form_viewset)
router.register(r'export_detail', Export_Detail_viewset)

urlpatterns = [
    path('', include(router.urls)),
    path('password_reset/', views.CustomResetPasswordRequestToken.as_view()),
    path('password_reset/confirm/', views.CustomResetPasswordConfirmView.as_view()),
]
