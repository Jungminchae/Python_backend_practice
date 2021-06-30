from django.urls import path
from .views import (
    PostListView,
    SinglePostView,
    category_page,
    tag_page,
    PostCreateView,
    PostUpdateView,
    new_comment,
    CommentUpdateView,
)


urlpatterns = [
    path("update_comment/<int:pk>/", CommentUpdateView.as_view()),
    path("update_post/<int:pk>/", PostUpdateView.as_view()),
    path("create_post/", PostCreateView.as_view()),
    path("tag/<str:slug>/", tag_page),
    path("category/<str:slug>/", category_page),
    path("<int:pk>/", SinglePostView.as_view()),
    path("<int:pk>/new_comment/", new_comment),
    path("", PostListView.as_view()),
]

