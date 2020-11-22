from django.views.generic import DetailView, ListView
from django.views.generic.dates import (
    ArchiveIndexView,
    YearArchiveView,
    MonthArchiveView,
)
from django.views.generic.dates import DayArchiveView, TodayArchiveView
from django.shortcuts import render
from blog.models import Post

# LV
class PostLV(ListView):
    model = Post
    template_name = "blog/post_all.html"
    context_object_name = "posts"
    paginate_by = 2


# DV
class PostDV(DetailView):
    model = Post


# ArchiveView
class PostAV(ArchiveIndexView):
    model = Post
    date_field = "modify_dt"


class PostYAV(YearArchiveView):
    model = Post
    date_field = "modify_dt"
    make_object_list = True


class PostMAV(MonthArchiveView):
    model = Post
    date_field = "modify_dt"


class PostDAV(DayArchiveView):
    model = Post
    date_field = "modify_dt"


class PostTAV(TodayArchiveView):
    model = Post
    date_field = "modify_dt"
