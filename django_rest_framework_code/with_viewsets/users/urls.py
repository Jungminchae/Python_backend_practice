from django.urls import path
from .views import UsersView, LikesView, login_view

app_name = "users"

urlpatterns = [
    path("", UsersView.as_view()),
    path("likes/", LikesView.as_view()),
    path("login/", login_view),
]
