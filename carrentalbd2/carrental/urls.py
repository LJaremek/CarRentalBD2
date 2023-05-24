from django.urls import path
from .views import about, profile


urlpatterns = [path("", about, name="home"),
               path("profile/", profile, name="profile")]
