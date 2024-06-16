from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path("stats/import_export/", views.StatsImportAndExportView.as_view()),
    path("stats/top5_export/", views.Top5PopularProductsView.as_view()),
    path("stats/total_import/", views.TotalImport.as_view()),
    path("stats/total_export/", views.ToltalExport.as_view()),
]
