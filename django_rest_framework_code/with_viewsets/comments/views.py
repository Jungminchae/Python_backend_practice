from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from .serializers import CommentSerializer
from .models import Comment
from questions.models import Question
from users.models import User


# 댓글 생성 View
class CommentView(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # 댓글을 달 질문의 pk나 title을 받아오면 될 것 같음
        question = Question.objects.get(pk=request.data.get("question"))
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment = serializer.save(username=request.user, question=question)
            comment_serializer = CommentSerializer(comment).data
            return Response(data=comment_serializer, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 질문에 달린 댓글 가져오는 View
class QuestionCommentsView(APIView):
    def get_comments(self, pk):
        try:
            comments = Comment.objects.filter(question=pk)
            return comments
        except Comment.DoesNotExist:
            return None

    def get(self, request, pk):
        comments = self.get_comments(pk)
        if comments is not None:
            serializer = CommentSerializer(comments, many=True).data
            return Response(data=serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
