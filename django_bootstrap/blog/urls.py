from django.urls import path
from .views import PostListView, SinglePostView


urlpatterns = [
    path("<int:pk>/", SinglePostView.as_view()),
    path("", PostListView.as_view()),
]

