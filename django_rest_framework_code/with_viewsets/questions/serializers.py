from rest_framework import fields, serializers
from users.serializers import UserSerializer
from .models import Question

# 질문 전체 serializer
class QuestionSerializer(serializers.ModelSerializer):

    username = UserSerializer()

    class Meta:
        model = Question
        fields = ("username", "id", "created_at", "updated_at")
        read_only_fields = ("username", "id", "created_at", "updated_at")


# 질문 생성 serializer
class CreateQuestionSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=500)

    def create(self, validated_data):
        return Question.objects.create(**validated_data)
