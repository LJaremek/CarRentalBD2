from django.urls import path
from .views import entry_page

urlpatterns = [path("", entry_page)]
