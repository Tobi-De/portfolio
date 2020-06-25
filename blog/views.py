from braces.views import SuperuserRequiredMixin, FormValidMessageMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import (
    View,
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)

from .forms import BlogPostForm, BlogPostContentForm
from .models import BlogPost
from .viewmixins import PostPublishedRequiredMixin


class BlogPostListView(ListView):
    queryset = BlogPost.objects.filter(status=BlogPost.STATUS.published)
    context_object_name = "blogposts"


class BlogPostCreateView(FormValidMessageMixin, SuperuserRequiredMixin, CreateView):
    model = BlogPost
    template_name = "blog/blogpost_create.html"
    form_class = BlogPostForm
    form_valid_message = "Blog post created"

    def get_success_url(self) -> str:
        blogpost = self.get_context_data().get("blogpost")
        return reverse("blog:blogpost_content_editor", kwargs={"slug": blogpost.slug})


class BlogPostContentEditorView(SuperuserRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        blogpost = get_object_or_404(BlogPost, slug=kwargs.get("slug"))
        form = BlogPostContentForm(initial={"body": blogpost.body})
        return render(request, "blog/blogpost_content_editor.html", {"form": form})

    def post(self, request, *args, **kwargs):
        blogpost = get_object_or_404(BlogPost, slug=kwargs.get("slug"))
        form = BlogPostContentForm(request.POST)
        if form.is_valid():
            blogpost.body = form.cleaned_data["body"]
            blogpost.save()
            return redirect("blog:blogpost_detail", slug=blogpost.slug)
        else:
            return redirect("blog:blogpost_content_editor", kwargs={"slug": blogpost})


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
