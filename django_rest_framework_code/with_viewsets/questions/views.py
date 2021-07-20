from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionSerializer
from .models import Question
from .permissions import IsMe


class QuestionViewSet(ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        elif self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def search_question(self, request):
        keyword = request.GET.get("keyword", None)
        # 제목 or 내용에 keyword가 포함된 object 필터링
        question_list = Question.objects.filter(
            Q(title__contains=keyword) | Q(content__contains=keyword)
        )

        # paginator
        paginator = self.paginator

        # 필터 되어 검색된 것이 있으면 return
        if len(question_list):
            result = paginator.paginate_queryset(question_list, request)
            serializer = QuestionSerializer(result, many=True).data
            return paginator.get_paginated_response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False)
    def question_create(self, request):
        if request.method == "POST":
            # 로그인 상태의 유저만 질문하기 가능
            if not request.user.is_authenticated:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            serializer = CreateQuestionSerializer(data=request.data)
            # 유효성검사
            if serializer.is_valid():
                question = serializer.save(username=request.user)
                question_serializer = QuestionSerializer(question).data
                # 생성된 질문과 200 return
                return Response(data=question_serializer, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=True)
    def monthly_top_question(self, request, pk):

        question = self.get_object()
        if question:
            # 특정된 질문의 작성 월 가져오고 그 월에 작성된 질문만 필터링
            month = question.created_at.month
            # 좋아요 내림차순 정렬
            monthly_questions = Question.objects.filter(
                created_at__month=month
            ).order_by("-likes")
            # 좋아요 수는 같을 수도 있기 때문에 리스트에 저장
            max_likes_obj_list = [monthly_questions[0]]
            # 남은 질문들을 순회하며 좋아요가 같으면 리스트에 추가 아니면 멈춤
            for q in monthly_questions[1:]:
                if max_likes_obj_list[0].like_count() == q.like_count():
                    max_likes_obj_list.append(q)
                else:
                    break
            serializer = QuestionSerializer(max_likes_obj_list, many=True).data
            return Response(data=serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
