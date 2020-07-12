from braces.views import SuperuserRequiredMixin, FormValidMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)

from newsletter.forms import SubscriptionForm
from .forms import BlogPostContentForm, CommentForm
from .models import Post, Series, Comment, Category
from .viewmixins import PostPublishedRequiredMixin


class NewPostView(SuperuserRequiredMixin, TemplateView):
    template_name = "blog/new_post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        drafts = Post.objects.filter(status=Post.STATUS.draft).order_by(
            "-created"
        )
        paginator = Paginator(drafts, 6)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        return context


class PublishPostView(SuperuserRequiredMixin, TemplateView):
    template_name = "blog/post_confirm_publish.html"

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs.get("slug"))
        post.publish()
        messages.success(request, "Post published")
        return redirect("blog:post_list")


class PostListView(ListView):
    context_object_name = "posts"
    paginate_by = 4

    def get_queryset(self):
        queryset = Post.objects.filter(status=Post.STATUS.published).order_by(
            "-publish_date"
        )
        category = self.request.GET.get("category")
        q = self.request.GET.get("q")
        if category:
            queryset = queryset.filter(categories__name=category)
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(body__icontains=q)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latests"] = Post.objects.filter(
            status=Post.STATUS.published
        ).order_by("-publish_date")[:3]
        context["categories"] = Category.objects.all()
        context["newsletter_form"] = SubscriptionForm()
        context["popular"] = Post.popular_posts()
        return context


class PostCreateView(FormValidMessageMixin, SuperuserRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_create.html"
    fields = [
        "thumbnail",
        "title",
        "overview",
        "status",
        "reading_time",
        "categories",
        "author",
        "series",
        "scheduled_publish_date",
    ]
    form_valid_message = "Blog post created"

    def get_success_url(self) -> str:
        post = self.get_context_data().get("post")
        return reverse("blog:post_content_editor", kwargs={"slug": post.slug})


class PostContentEditorView(SuperuserRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs.get("slug"))
        form = BlogPostContentForm(initial={"body": post.body})
        return render(
            request,
            "blog/post_content_editor.html",
            {"form": form, "slug": post.slug},
        )

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs.get("slug"))
        form = BlogPostContentForm(request.POST)
        if form.is_valid():
            post.body = form.cleaned_data["body"]
            post.save()
            messages.success(request, "Post Updated")
            return redirect("blog:post_detail", slug=post.slug)
        else:
            return redirect("blog:post_content_editor", kwargs={"slug": post})


class PostDetailView(PostPublishedRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["newsletter_form"] = SubscriptionForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(post=self.get_object(), **form.cleaned_data)
        return redirect("blog:post_detail", slug=self.get_object().slug)


class PostUpdateView(
    SuperuserRequiredMixin,
    PostPublishedRequiredMixin,
    FormValidMessageMixin,
    UpdateView,
):
    model = Post
    template_name = "blog/post_update.html"
    fields = [
        "thumbnail",
        "title",
        "overview",
        "status",
        "categories",
        "author",
        "series",
        "scheduled_publish_date",
    ]
    form_valid_message = "Blog post updated"


class PostDeleteView(SuperuserRequiredMixin, FormValidMessageMixin, DeleteView):
    model = Post
    form_valid_message = "Blog post deleted"

    def get_success_url(self) -> str:
        return reverse("blog:post_list")


class SeriesCreateView(CreateView):
    model = Series
    fields = ["thumbnail", "title", "overview", "body", "status", "author"]
    template_name = "blog/series_create.html"


class SeriesListView(ListView):
    model = Series
    ordering = ["-created"]
    paginate_by = 4
    context_object_name = "series"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latests"] = self.get_queryset()[:3]
        context["categories"] = Category.objects.all()
        context["newsletter_form"] = SubscriptionForm()
        context["popular"] = Post.popular_posts()
        return context


class SeriesDetailView(DetailView):
    model = Series

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["newsletter_form"] = SubscriptionForm()
        return context


class SeriesUpdateView(
    SuperuserRequiredMixin, FormValidMessageMixin, UpdateView
):
    model = Series
    fields = ["thumbnail", "title", "overview", "body", "status", "author"]
    template_name = "blog/series_update.html"
    form_valid_message = "Blog Series Updated"


class SeriesDeleteView(
    SuperuserRequiredMixin, FormValidMessageMixin, DeleteView
):
    model = Series
    form_valid_message = "Blogpost Series Deleted"

    def get_success_url(self):
        return reverse("blog:series_list")
