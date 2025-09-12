from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render


def landing_page(request):
    return render(
        request,
        "landing.html",
    )


def custom_login(request):
    return render(request, "login.html")


class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "You have been logged out successfully.")
        return redirect("landing")
