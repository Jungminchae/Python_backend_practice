from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator


class Student(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.SlugField(
        blank=True, null=True, validators=[RegexValidator("[a-zA-Z]+")]
    )
    admission_number = models.IntegerField(unique=True)
    is_qualified = models.BooleanField(default=False)
    average_score = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.first_name

    def get_grade(self):
        if 0 <= self.average_score < 40:
            return "Fail"
        elif 40 <= self.average_score < 70:
            return "Pass"
        elif 70 <= self.average_score <= 100:
            return "Excellent"
        else:
            return "Error"

    def save(self, *args, **kwargs):
        self.username = slugify(self.first_name)
        super(Student, self).save(*args, **kwargs)


class ClassRoom(models.Model):
    name = models.CharField(max_length=120)
    student_capacity = models.IntegerField()
    students = models.ManyToManyField("classrooms.Student")

    def __str__(self) -> str:
        return self.name
