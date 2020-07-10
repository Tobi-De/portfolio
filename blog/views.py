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
from .models import BlogPost, BlogPostSeries, Comment, Category
from .viewmixins import PostPublishedRequiredMixin


class NewPostView(SuperuserRequiredMixin, TemplateView):
    template_name = "blog/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        drafts = BlogPost.objects.filter(status=BlogPost.STATUS.draft).order_by(
            "-created"
        )
        paginator = Paginator(drafts, 6)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        return context


class PublishPostView(SuperuserRequiredMixin, TemplateView):
    template_name = "blog/blogpost_confirm_publish.html"

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(BlogPost, slug=kwargs.get("slug"))
        post.publish()
        messages.success(request, "Post published")
        return redirect("blog:blogpost_list")


class BlogPostListView(ListView):
    context_object_name = "blogposts"
    paginate_by = 4

    def get_queryset(self):
        queryset = BlogPost.objects.filter(status=BlogPost.STATUS.published).order_by(
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
        context["latests"] = BlogPost.objects.filter(
            status=BlogPost.STATUS.published
        ).order_by("-publish_date")[:3]
        context["categories"] = Category.objects.all()
        context["newsletter_form"] = SubscriptionForm()
        return context


class BlogPostCreateView(FormValidMessageMixin, SuperuserRequiredMixin, CreateView):
    model = BlogPost
    template_name = "blog/blogpost_create.html"
    fields = [
        "thumbnail",
        "title",
        "overview",
        "status",
        "categories",
        "author",
        "blogpostseries",
        "scheduled_publish_date",
    ]
    form_valid_message = "Blog post created"

    def get_success_url(self) -> str:
        blogpost = self.get_context_data().get("blogpost")
        return reverse("blog:blogpost_content_editor", kwargs={"slug": blogpost.slug})


class BlogPostContentEditorView(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        blogpost = get_object_or_404(BlogPost, slug=kwargs.get("slug"))
        form = BlogPostContentForm(initial={"body": blogpost.body})
        return render(
            request,
            "blog/blogpost_content_editor.html",
            {"form": form, "slug": blogpost.slug},
        )

    def post(self, request, *args, **kwargs):
        blogpost = get_object_or_404(BlogPost, slug=kwargs.get("slug"))
        form = BlogPostContentForm(request.POST)
        if form.is_valid():
            blogpost.body = form.cleaned_data["body"]
            blogpost.save()
            messages.success(request, "Post Updated")
            return redirect("blog:blogpost_detail", slug=blogpost.slug)
        else:
            return redirect("blog:blogpost_content_editor", kwargs={"slug": blogpost})


class BlogPostDetailView(PostPublishedRequiredMixin, DetailView):
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["newsletter_form"] = SubscriptionForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(blogpost=self.get_object(), **form.cleaned_data)
        return redirect("blog:blogpost_detail", slug=self.get_object().slug)


class BlogPostUpdateView(
    SuperuserRequiredMixin,
    PostPublishedRequiredMixin,
    FormValidMessageMixin,
    UpdateView,
):
    model = BlogPost
    template_name = "blog/blogpost_update.html"
    fields = [
        "thumbnail",
        "title",
        "overview",
        "status",
        "categories",
        "author",
        "blogpostseries",
        "scheduled_publish_date",
    ]
    form_valid_message = "Blog post updated"


class BlogPostDeleteView(SuperuserRequiredMixin, FormValidMessageMixin, DeleteView):
    model = BlogPost
    form_valid_message = "Blog post deleted"

    def get_success_url(self) -> str:
        return reverse("blog:blogpost_list")


class BlogPostSeriesCreateView(CreateView):
    model = BlogPostSeries
    fields = ["thumbnail", "title", "overview", "body", "status", "author"]
    template_name = "blog/blogpostseries_create.html"


class BlogPostSeriesListView(ListView):
    model = BlogPostSeries
    ordering = ["-created"]
    paginate_by = 4
    context_object_name = "series"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latests"] = self.get_queryset()[:3]
        context["categories"] = Category.objects.all()
        context["newsletter_form"] = SubscriptionForm()
        return context


class BlogPostSeriesDetailView(DetailView):
    model = BlogPostSeries

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["newsletter_form"] = SubscriptionForm()
        return context


class BlogPostSeriesUpdateView(
    SuperuserRequiredMixin, FormValidMessageMixin, UpdateView
):
    model = BlogPostSeries
    fields = ["thumbnail", "title", "overview", "body", "status", "author"]
    template_name = "blog/blogpostseries_update.html"
    form_valid_message = "Blog Series Updated"


class BlogPostSeriesDeleteView(
    SuperuserRequiredMixin, FormValidMessageMixin, DeleteView
):
    model = BlogPostSeries
    form_valid_message = "Blogpost Series Deleted"

    def get_success_url(self):
        return reverse("blog:blogpostseries_list")
