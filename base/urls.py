from django.urls import path

from . import views

urlpatterns = [
    path('password_reset/', views.CustomResetPasswordRequestToken.as_view()),
    path('password_reset/confirm/', views.CustomResetPasswordConfirmView.as_view()),
]
