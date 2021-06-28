from django.views.generic import ListView, DetailView
from .models import Post

# listview 쓸거임
# def index(request):
#     posts = Post.objects.all().order_by("-pk")

#     return render(request, "blog/index.html", {"posts": posts})


class PostListView(ListView):
    model = Post
    template_name = "blog/index.html"
    ordering = "-pk"
    context_object_name = "posts"


# detail view 쓸거임
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)

#     return render(request, "blog/single_page.html", {"post": post})


class SinglePostView(DetailView):
    model = Post
    template_name = "blog/single_page.html"
