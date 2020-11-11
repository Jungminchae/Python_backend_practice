import json
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from blogs import models as blogs_models

class HomeView(ListView):

    model = blogs_models.Post
    paginate_by = 10 
    paginate_orphans = 5
    ordering = "-created"
    context_object_name = "posts"


def post_detail(request, post_id):
    post = get_object_or_404(blogs_models.Post, pk=post_id)
    comments = blogs_models.Comment.objects.filter(post=post.id)
    is_liked = False

    if post.likes.filter(id=request.user.id).exists():
        is_liked = False
    return render(request, "blogs/post_detail.html", context={"post":post, "comments":comments, 'is_liked':is_liked, 'total_likes':post.total_likes()})