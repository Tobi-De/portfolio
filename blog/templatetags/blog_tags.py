from django import template

from ..models import Post

register = template.Library()


@register.filter()
def tag_post_count(value):
    return Post.published_post().filter(tags__in=[value]).count()
