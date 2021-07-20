from django.db import models
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ("updated_at",)
        read_only_fields = ("id", "username", "question")
