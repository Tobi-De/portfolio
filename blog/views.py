from braces.views import SuperuserRequiredMixin, FormValidMessageMixin
from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)

from .forms import BlogPostForm
from .models import BlogPost
from .viewmixins import PostPublishedRequiredMixin


class BlogPostListView(ListView):
    queryset = BlogPost.objects.filter(status=BlogPost.STATUS.published)
    context_object_name = "blogposts"


class BlogPostCreateView(FormValidMessageMixin, CreateView):
    model = BlogPost
    template_name = "blog/blogpost_create.html"
    form_class = BlogPostForm
    form_valid_message = "Blog post created"


class BlogPostDetailView(PostPublishedRequiredMixin, FormValidMessageMixin, DetailView):
    model = BlogPost


class BlogPostUpdateView(SuperuserRequiredMixin, PostPublishedRequiredMixin, FormValidMessageMixin, UpdateView):
    model = BlogPost
    template_name = "blog/blogpost_update.html"
    form_class = BlogPostForm
    form_valid_message = "Blog post updated"


class BlogPostDeleteView(SuperuserRequiredMixin, FormValidMessageMixin, DeleteView):
    model = BlogPost
    form_valid_message = "Blog post deleted"

    def get_success_url(self) -> str:
        return reverse("blog:blogpost_list")


class BlogPostSeriesCreateView(CreateView):
    model = BlogPost
