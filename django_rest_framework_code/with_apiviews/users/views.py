import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UserSerializer
from questions.serializers import QuestionSerializer
from questions.models import Question

# 유저 생성 View
class UsersView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(UserSerializer(new_user).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 좋아요 View
class LikesView(APIView):
    # 로그인된 유저만 좋아요 가능
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = QuestionSerializer(user.likes.all(), many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def put(self, request):
        # 질문 번호
        pk = request.data.get("pk", None)
        user = request.user
        if pk is not None:
            try:
                # 질문 번호에 맞는 질문 가져오기
                question = Question.objects.get(pk=pk)
                # 이미 좋아요 했으면 좋아요 취소 안했으면 좋아요
                if question in user.likes.all():
                    user.likes.remove(question)
                else:
                    user.likes.add(question)
                return Response()
            except Question.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# login view
@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # authentication이 되면 username이 반환됨
    user = authenticate(username=username, password=password)
    if user is not None:
        # jwt 는 해독을 못하게 하는게 목적이 아니고 token을 누가 수정했는지 안했는지를 확인하는 목적
        encoded_jwt = jwt.encode(
            {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
        )
        return Response(data={"token": encoded_jwt})
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
