"""
URL configuration for carrentalbd2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from carrental.views import log_screen_view, check_log
from django.contrib.auth import views as auth_views
from carrental.views import (
    log_screen_view,
    check_log,
    registration_person,
    registration_company,
    car_rent,
    main_window,
    my_account,
    car_cancel
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("base/", log_screen_view, name="base"),
    path("check_log/", check_log, name="check_log"),
    path("logout_user/", auth_views.LogoutView.as_view(template_name="logout_user.html"), name="logout_user"),
    path("registration_person/", registration_person, name="registration_person"),
    path("registration_company/", registration_company, name="registration_company"),
    path("my_account/", my_account, name="my_account"),
    path("car_rent/", car_rent, name="car_rent"),
    path("car_cancel/", car_cancel, name="car_cancel"),
    path("main_window/", main_window, name="main_window")
]
