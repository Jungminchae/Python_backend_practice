from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import QuestionSerializer, CreateQuestionSerializer
from .models import Question

# 여러 view에서 사용되어 global 함수로 선언
# object get or None
def get_object(pk):
    try:
        question = Question.objects.get(pk=pk)
        return question
    except Question.DoesNotExist:
        return None


# 특정 질문 읽기, 수정, 삭제
class QuestionView(APIView):
    def get(self, request, pk):
        question = get_object(pk)
        if question is not None:
            serializer = QuestionSerializer(question).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        question = get_object(pk)
        if question is not None:
            # 글쓴이가 아니고 다른 유저가 수정을 할 수 없음 403
            if question.username != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # 제목 or 내용 수정 가능 partial = True
            serializer = QuestionSerializer(question, data=request.data, partial=True)
            # 유효성 검사
            if serializer.is_valid():
                question = serializer.save()
                return Response(QuestionSerializer(question).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        question = get_object(pk)
        if question is not None:
            # 글쓴이가 아니고 다른 유저가 삭제를 할 수 없음 403
            if question.username != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            question.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# 질문 생성 view
@api_view(["POST"])
def question_create_view(request):
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
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def search_question_view(request, keyword):
    if request.method == "GET":
        # 제목 or 내용에 keyword가 포함된 object 필터링
        question_list = Question.objects.filter(
            Q(title__contains=keyword) | Q(content__contains=keyword)
        )
        # 필터 되어 검색된 것이 있으면 return
        if len(question_list):
            serializer = QuestionSerializer(question_list, many=True).data
            return Response(data=serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# 질문 작성일 기준/ 각 월별 전체 질문 중에서 /가장 좋아요가 많은 질문을/ 출력하는 API 개발
# 문제가 잘 이해되지 않아서, 특정 질문을 선택했을 때 그 질문의 작성일 기준 월 전체 질문 중에서
# 가장 좋아요 많은 질문을 출력하는 API로 작성했습니다
@api_view(["GET"])
def monthly_top_question_view(request, pk):

    if request.method == "GET":
        question = get_object(pk)

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
