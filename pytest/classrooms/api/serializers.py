from rest_framework import serializers
from classrooms.models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            "first_name",
            "last_name",
            "username",
            "admission_number",
            "is_qualified",
            "average_score",
        )
