from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category

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
