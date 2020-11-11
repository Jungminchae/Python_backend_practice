from django.db import models
from taggit.managers import TaggableManager
from core import models as core_models 
from users import models as user_models

class Post(core_models.TimeStampedModel):
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    likes = models.ManyToManyField(user_models.User, related_name='likes', blank=True)
    tags = TaggableManager()

    def __str__(self):
        return f"{self.id} - {self.title}"

    def total_likes(self):
        return self.likes.count()


class Comment(core_models.TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.id} - {self.user}"