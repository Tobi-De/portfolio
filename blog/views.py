from braces.views import SuperuserRequiredMixin, FormValidMessageMixin
from django.db.models import Q
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

from .forms import BlogPostContentForm, CommentForm
from .models import BlogPost, BlogPostSeries
from .viewmixins import PostPublishedRequiredMixin


class HomeView(View):

    def get(self, request, *args, **kwargs):
        context = {
            "recent_posts": BlogPost.objects.filter(status=BlogPost.STATUS.published).order_by("-created")[:3],
            "recent_series": BlogPostSeries.objects.all().order_by("-created")[:3]
        }
        return render(request, "blog/home.html", context)

    def post(self, request, *args, **kwargs):
        pass


class BlogPostListView(ListView):
    context_object_name = "blogposts"
    paginate_by = 5

    def get_queryset(self):
        queryset = BlogPost.objects.filter(status=BlogPost.STATUS.published).order_by("-created")
        category = self.request.GET.get("category")
        q = self.request.GET.get("q")
        if category:
            queryset = queryset.filter(categories__name=category)
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(body__icontains=q)).distinct()
        return queryset


class BlogPostCreateView(FormValidMessageMixin, SuperuserRequiredMixin, CreateView):
    model = BlogPost
    template_name = "blog/blogpost_create.html"
    fields = [
        "thumbnail", "title", "status", "categories", "author", "blogpostseries", "scheduled_publish_date"
    ]
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


class BlogPostDetailView(PostPublishedRequiredMixin, DetailView):
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context


class BlogPostUpdateView(SuperuserRequiredMixin, PostPublishedRequiredMixin, FormValidMessageMixin, UpdateView):
    model = BlogPost
    template_name = "blog/blogpost_update.html"
    fields = [
        "thumbnail", "title", "status", "categories", "author", "blogpostseries", "scheduled_publish_date"
    ]
    form_valid_message = "Blog post updated"


class BlogPostDeleteView(SuperuserRequiredMixin, FormValidMessageMixin, DeleteView):
    model = BlogPost
    form_valid_message = "Blog post deleted"

    def get_success_url(self) -> str:
        return reverse("blog:blogpost_list")


class BlogPostSeriesCreateView(CreateView):
    model = BlogPostSeries
    fields = ["thumbnail", "title", "body", "status", "author"]
    template_name = "blog/blogpostseries_create.html"


class BlogPostSeriesListView(ListView):
    model = BlogPostSeries
    ordering = ["-created"]
    paginate_by = 5
    context_object_name = "series"


class BlogPostSeriesDetailView(DetailView):
    model = BlogPostSeries


class BlogPostSeriesUpdateView(SuperuserRequiredMixin, FormValidMessageMixin, UpdateView):
    model = BlogPostSeries
    fields = ["thumbnail", "title", "body", "status", "author"]
    template_name = "blog/blogpostseries_update.html"
    form_valid_message = "Blog Series Created"


class BlogPostSeriesDeleteView(SuperuserRequiredMixin, FormValidMessageMixin, DeleteView):
    model = BlogPostSeries
    form_valid_message = "Blogpost Series Deleted"

    def get_success_url(self):
        return reverse("blog:blogpostseries_list")
