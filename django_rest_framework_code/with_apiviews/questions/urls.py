from django.urls import path
from .views import (
    QuestionView,
    question_create_view,
    search_question_view,
    monthly_top_question_view,
)

app_name = "questions"

urlpatterns = [
    path("<int:pk>/", QuestionView.as_view()),
    path("", question_create_view),
    path("search/<str:keyword>/", search_question_view),
    path("monthly_top/<int:pk>/", monthly_top_question_view),
]

