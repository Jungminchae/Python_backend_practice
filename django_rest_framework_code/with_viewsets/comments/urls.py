from django.urls import path
from .views import CommentView, QuestionCommentsView

app_name = "comments"

urlpatterns = [
    path("", CommentView.as_view()),
    path("<int:pk>/", QuestionCommentsView.as_view()),
]

