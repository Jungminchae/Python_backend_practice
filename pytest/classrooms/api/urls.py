from django.urls import path

from .views import StudentListAPIView

urlpatterns = [path("list/", StudentListAPIView.as_view(), name="student-list-api")]
