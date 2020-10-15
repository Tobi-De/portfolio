from braces.views import SuperuserRequiredMixin, FormValidMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
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
from .forms import BlogPostContentForm, PostForm, SeriesForm
from .helpers import postable_add_extra_context, post_filter
from .models import Post, Series


class NewPostView(SuperuserRequiredMixin, TemplateView):
    template_name = "blog/new_post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        drafts = Post.objects.filter(status=Post.STATUS.draft).order_by("-created")
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
    paginate_by = 8

    def get_queryset(self):
        queryset = Post.objects.filter(status=Post.STATUS.published).order_by(
            "-publish_date"
        )
        filtered_post = post_filter(self.request, queryset=queryset)
        return filtered_post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        postable_add_extra_context(context=context)
        return context


class PostCreateView(FormValidMessageMixin, SuperuserRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_create.html"
    form_class = PostForm
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


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_published and not self.request.user.is_superuser:  # noqa
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["newsletter_form"] = SubscriptionForm()
        return context


class SecretKeyPostDetailView(DetailView):
    model = Post
    slug_url_kwarg = "secret_key"
    slug_field = "secret_key"
    template_name = "blog/post_detail.html"

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        if post.is_published:  # noqa
            return redirect(post.get_absolute_url())  # noqa
        return super().get(request, *args, **kwargs)


class PostUpdateView(
    SuperuserRequiredMixin,
    FormValidMessageMixin,
    UpdateView,
):
    model = Post
    template_name = "blog/post_update.html"
    form_class = PostForm
    form_valid_message = "Blog post updated"


class PostDeleteView(SuperuserRequiredMixin, FormValidMessageMixin, DeleteView):
    model = Post
    form_valid_message = "Blog post deleted"

    def get_success_url(self) -> str:
        return reverse("blog:post_list")


class SeriesCreateView(CreateView):
    model = Series
    form_class = SeriesForm
    template_name = "blog/series_create.html"


class SeriesListView(ListView):
    queryset = Series.objects.filter(visible=True).order_by("created")
    paginate_by = 8
    context_object_name = "series"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        postable_add_extra_context(context=context)
        return context


class SeriesDetailView(DetailView):
    model = Series

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["newsletter_form"] = SubscriptionForm()
        return context


class SeriesUpdateView(SuperuserRequiredMixin, FormValidMessageMixin, UpdateView):
    model = Series
    form_class = SeriesForm
    template_name = "blog/series_update.html"
    form_valid_message = "Blog Series Updated"


class SeriesDeleteView(SuperuserRequiredMixin, FormValidMessageMixin, DeleteView):
    model = Series
    form_valid_message = "Blogpost Series Deleted"

    def get_success_url(self):
        return reverse("blog:series_list")
