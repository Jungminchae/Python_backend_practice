import pytest
from django.urls import reverse
from mixer.backend.django import mixer
from classrooms.models import Student
from rest_framework.test import APIClient, APITestCase

pytestmark = pytest.mark.django_db


class TestStudentAPIView(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_student_list_works(self):
        student = mixer.blend(Student, first_name="Geoffrey")

        url = reverse("student-list-api")
        response = self.client.get(url)

        assert response.status_code == 200
