from django.db import models
from core.models import CoreModel
from questions.models import Question
from users.models import User


class Comment(CoreModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
