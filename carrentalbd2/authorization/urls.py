from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [path("register_user/", views.register_user, name="auth/register_user"),
               path("login_user/", auth_views.LoginView.as_view(template_name="login_user.html"), name="auth/login_user"),
               path("logout_user/", auth_views.LogoutView.as_view(template_name="logout_user.html"), name="auth/logout_user"),]