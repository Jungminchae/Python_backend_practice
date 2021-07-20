from rest_framework import fields, serializers
from users.serializers import UserSerializer
from .models import Question

# 질문 전체 serializer
class QuestionSerializer(serializers.ModelSerializer):

    username = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = ("username", "id", "created_at", "updated_at")

