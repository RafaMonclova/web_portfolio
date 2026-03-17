from .views import about_detail
from django.urls import path

urlpatterns = [
    path("", about_detail, name="about"),
]