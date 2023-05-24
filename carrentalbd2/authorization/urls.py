from django.urls import path
from . import views

urlpatterns = [path("login_user/", views.login_user, name="auth/login_user"),
               path("register_user/", views.register_user, name="auth/register_user")]
