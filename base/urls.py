from . import views
from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"depot", Depotviewset)
router.register(r"profile", Profileviewset)
router.register(r"business_Partner", BusinessPartnerviewset)
router.register(r"category", Categoryviewset)
router.register(r"product", Productviewset)
router.register(r"product_depot", ProductDepotviewset)
router.register(r"pricelist", Pricelistviewset)
router.register(r"product_price", ProductPriceviewset)
router.register(r"order_form", OrderFormviewset)
router.register(r"order_detail", OrderDetailviewset)
router.register(r"import_form", ImportFormviewset)
router.register(r"import_detail", ImportDetailviewset)
router.register(r"export_form", ExportFormviewset)
router.register(r"export_detail", ExportDetailviewset)

urlpatterns = [
    path("", include(router.urls)),
    path("password_reset/", views.CustomResetPasswordRequestToken.as_view()),
    path("password_reset/confirm/", views.CustomResetPasswordConfirmView.as_view()),
    path("change_password/", views.ReplacePassword.as_view()),
    path("get_order_from_depot/", views.GetOrderFromDepotAPIView.as_view()),
    path("get_order_dont_have_import/", views.GetOrderDontHaveImport.as_view()),
    path("download_excel/", views.ExcelFileDownloadView.as_view()),
    path("upload_excel/", views.ExcelFileUploadView.as_view()),
]
