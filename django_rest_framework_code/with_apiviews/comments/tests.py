from rest_framework import response
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from users.models import User
from questions.models import Question
from comments.models import Comment


class CommentViewTest(APITestCase):
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

        # Dummy Comment
        self.comment_1 = Comment.objects.create(
            question=self.question_1, username=self.test_user_2, content="1번글에 2번이 댓글달음"
        )
        self.comment_2 = Comment.objects.create(
            question=self.question_1, username=self.test_user_3, content="1번글에 3번이 댓글달음"
        )

    def test_question_comments(self):
        question_pk = 1
        url = f"http://127.0.0.1:8000/comments/{question_pk}/"
        # 두개의 댓글이 나와야 함
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_make_comment(self):
        url = "http://127.0.0.1:8000/comments/"
        data = {"question": 1, "content": "1번글에 1번이 댓글달음"}

        # 기존 댓글 2개에서 댓글 달리면 3개가 되어야 함
        response_1 = self.client.post(url, data, format="json")
        response_2 = self.client.get("http://127.0.0.1:8000/comments/1/", format="json")

        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(len(response_2.data), 3)
