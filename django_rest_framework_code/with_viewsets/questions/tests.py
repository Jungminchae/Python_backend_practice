from rest_framework import response
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from users.models import User
from .models import Question


class QuestionViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user_1 = User.objects.create_user(
            username="test_1", email="test@test.com", password="test123456879"
        )
        self.client.login(username="test_1", password="test123456879")

        self.test_user_2 = User.objects.create_user(
            username="test_2", email="test2@test.com", password="test123456879"
        )
        self.test_user_3 = User.objects.create_user(
            username="test_3", email="test3@test.com", password="test123456879"
        )
        self.question_1 = Question.objects.create(
            username=self.test_user_1, title="test_1", content="content_1",
        )
        self.question_2 = Question.objects.create(
            username=self.test_user_2, title="test_2", content="content_2",
        )
        self.question_3 = Question.objects.create(
            username=self.test_user_3, title="test_3", content="content_3",
        )
        self.question_4 = Question.objects.create(
            username=self.test_user_1,
            title="test1의 2번째 글",
            content="_1로 검색하면 2개가 나오겠지?",
        )

    def test_question_create(self):
        url = "http://127.0.0.1:8000/questions/"
        data = {"title": "test_1", "content": "content_1"}
        # 질문 생성
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.question_1.title, response.data.get("title"))
        self.assertEqual(self.question_1.content, response.data.get("content"))

    def test_question_edit_delete(self):
        url = "http://127.0.0.1:8000/questions/1/"
        data = {"title": "test_1!"}
        # 질문 수정
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.question_1.title, response.data.get("title"))

        # 질문 삭제
        response_2 = self.client.delete(url, format="json")
        # 질문 삭제 후 404 에러가 나와야함
        response_3 = self.client.get(url, format="json")

        self.assertEqual(response_3.status_code, 404)

    def test_question_search(self):
        keyword = "_1"
        url = f"http://127.0.0.1:8000/questions/search/{keyword}/"

        # 질문 검색
        # 질문이 2개가 검색 되어야함
        response = self.client.get(url, format="json")

        self.assertEqual(len(response.data), 2)
