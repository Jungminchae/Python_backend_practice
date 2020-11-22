from django.db import models

class Bookmark(models.Model):
    title = models.CharField("TITLE", max_length=100, blank=True) # verbose_name = TITLE 
    url = models.URLField("URL", unique=True) # verbose_name = URL

    def __str__(self):
        return self.title

