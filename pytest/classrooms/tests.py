import pytest
from hypothesis import strategies as st, given
from hypothesis.extra.django import TestCase
from classrooms.models import Student, ClassRoom
from mixer.backend.django import mixer


pytestmark = pytest.mark.django_db


class TestStudent(TestCase):
    def test_student_can_be_created(self):
        student = mixer.blend(Student)

        student_result = Student.objects.all()

        assert student_result.exists(), True

    @given(st.floats(min_value=0, max_value=40))
    def test_grade_fail(self, fail_score):

        print(fail_score)

        student1 = mixer.blend(Student, average_score=fail_score)
        student_result = Student.objects.last()
        assert student_result.get_grade() == "Fail"

    # @given(regex("[a-zA-Z0-9]+"))
    # def test_slugify(self, name):

    #     student1 = mixer.blend(Student, first_name=name)
    #     student_result = Student.objects.last()
    #     assert len(str(student_result.username)) == len(name)


class TestClassRoom:
    def test_classroom_create(self):
        classroom = mixer.blend(ClassRoom, name="Physics")
        classroom_result = ClassRoom.objects.last()

        assert str(classroom_result) == "Physics"
