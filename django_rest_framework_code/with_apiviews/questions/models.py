from django.db import models
from users.models import User
from core.models import CoreModel


class Question(CoreModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def like_count(self):
        return self.likes.count()
