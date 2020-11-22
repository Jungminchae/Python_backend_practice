from django.urls import path
from .views import BookmarkDV, BookmarkLV

app_name = "bookmark"

urlpatterns = [
    path("bookmark/<int:pk>/", BookmarkDV.as_view(), name="detail"),
    path("bookmark/", BookmarkLV.as_view(), name="index"),
]

