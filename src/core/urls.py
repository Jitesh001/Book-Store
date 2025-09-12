from django.urls import path

from .views import CustomLogoutView, custom_login, landing_page

urlpatterns = [
    path("", landing_page, name="landing"),
    path("login/", custom_login, name="login"),
    path("accounts/logout/", CustomLogoutView.as_view(), name="account_logout"),
]
