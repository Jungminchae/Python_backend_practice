from django.urls import path
from .views import landing, about_me

urlpatterns = [path("about/", about_me), path("", landing)]

