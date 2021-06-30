from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .models import Post, Category, Tag


# listview 쓸거임
# def index(request):
#     posts = Post.objects.all().order_by("-pk")

#     return render(request, "blog/index.html", {"posts": posts})


class PostListView(ListView):
    model = Post
    template_name = "blog/index.html"
    ordering = "-pk"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data()
        context["categories"] = Category.objects.all()
        context["no_category_post_count"] = Post.objects.filter(category=None).count()
        return context


# detail view 쓸거임
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)

#     return render(request, "blog/single_page.html", {"post": post})


class SinglePostView(DetailView):
    model = Post
    template_name = "blog/single_page.html"

    def get_context_data(self, **kwargs):
        context = super(SinglePostView, self).get_context_data()
        context["categories"] = Category.objects.all()
        context["no_category_post_count"] = Post.objects.filter(category=None).count()
        return context


def category_page(request, slug):
    if slug == "no_category":
        category = "미분류"
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        "blog/index.html",
        {
            "posts": post_list,
            "categories": Category.objects.all(),
            "no_category_post_count": Post.objects.filter(category=None).count(),
            "category": category,
        },
    )


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        "blog/index.html",
        {
            "posts": post_list,
            "categories": Category.objects.all(),
            "no_category_post_count": Post.objects.filter(category=None).count(),
            "tag": tag,
        },
    )


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = [
        "title",
        "hook_text",
        "content",
        "head_image",
        "file_upload",
        "category",
    ]

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (
            current_user.is_staff or current_user.is_superuser
        ):
            form.instance.author = current_user
            return super(PostCreateView, self).form_valid(form)
        else:
            return redirect("/blog/")


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = [
        "title",
        "hook_text",
        "content",
        "head_image",
        "file_upload",
        "category",
    ]
    template_name = "blog/post_update_form.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
