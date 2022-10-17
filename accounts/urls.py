from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
]