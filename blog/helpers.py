from django.db.models import Q

from newsletter.forms import SubscriptionForm
from .models import Post, Category


def postable_add_extra_context(context):
    # add needed data in context for sidebars
    context["featured"] = Post.objects.filter(
        featured=True, status=Post.STATUS.published
    ).order_by("-created")
    context["categories"] = Category.objects.all()
    context["newsletter_form"] = SubscriptionForm()
    context["coming_soon"] = Post.objects.filter(status=Post.STATUS.draft).order_by(
        "-created"
    )[:2]


def post_filter(request, queryset):
    q = request.GET.get("q")
    category = request.GET.get("category")
    if category:
        queryset = queryset.filter(categories__name=category)
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q) | Q(body__icontains=q) | Q(overview__contains=q)
        ).distinct()
    return queryset
