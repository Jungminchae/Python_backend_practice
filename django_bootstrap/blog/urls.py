from django.urls import path
from .views import (
    PostListView,
    SinglePostView,
    category_page,
    tag_page,
    PostCreateView,
    PostUpdateView,
)


urlpatterns = [
    path("update_post/<int:pk>/", PostUpdateView.as_view()),
    path("create_post/", PostCreateView.as_view()),
    path("tag/<str:slug>/", tag_page),
    path("category/<str:slug>/", category_page),
    path("<int:pk>/", SinglePostView.as_view()),
    path("", PostListView.as_view()),
]

