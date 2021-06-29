from django.urls import path
from .views import PostListView, SinglePostView, category_page


urlpatterns = [
    path("category/<str:slug>/", category_page),
    path("<int:pk>/", SinglePostView.as_view()),
    path("", PostListView.as_view()),
]

