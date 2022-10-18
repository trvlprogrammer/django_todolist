from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .api import LoginAPI, RegisterAPI
from knox import views as knox_views
from rest_framework import routers




app_name = "accounts"   

urlpatterns = [
    path("register", views.register, name="register"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("login", auth_views.LoginView.as_view(template_name="accounts/login_form.html"), name="login"),
    path(
        "change-password/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/change_password_form.html",
            success_url = "/"
        ),
        name="change_password"
    ),
    path("password_reset", views.password_reset_request, name="password_reset"),

    # knox auth api
    path('api/auth', include('knox.urls')),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name="knox_logout"),
]