from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # 기본 AbstractUser에 좋아요 field 추가
    likes = models.ManyToManyField(
        "questions.Question", related_name="likes", blank=True,
    )

