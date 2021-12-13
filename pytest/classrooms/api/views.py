from rest_framework.generics import ListAPIView
from classrooms.api.serializers import StudentSerializer
from classrooms.models import Student


class StudentListAPIView(ListAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
