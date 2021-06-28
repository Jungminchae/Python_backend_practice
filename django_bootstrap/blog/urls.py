from django.urls import path
from .views import index, single_post_page


urlpatterns = [path("<int:pk>/", single_post_page), path("", index)]

