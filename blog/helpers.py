from django.db.models import Q
from taggit.models import Tag

from newsletter.forms import SubscriptionForm
from .models import Post


def postable_add_extra_context(context):
    # add needed data in context for sidebars
    context["featured"] = Post.objects.filter(
        featured=True, status=Post.STATUS.published
    ).order_by("-created")
    context["tags"] = Tag.objects.all()
    context["newsletter_form"] = SubscriptionForm()
    context["coming_soon"] = (
        Post.objects.filter(status=Post.STATUS.draft)
            .exclude(title__icontains="!NeverComingSoon!")
            .order_by("-modified", "-created")[:3]
    )
    # !NeverComingSoon! A special string to add when I need
    # some post to never appear in the coming soon section


def post_filter(request, tag, queryset):
    q = request.GET.get("q")
    if tag:
        queryset = queryset.filter(tags__name__in=[tag])
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q) | Q(body__icontains=q) | Q(overview__contains=q)
        ).distinct()
    return queryset
