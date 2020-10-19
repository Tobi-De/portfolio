from django.template.loader import render_to_string
from django.utils import timezone

from blog.models import Post
from .models import News


def send_news_task(key_identifier):
    try:
        News.objects.get(key_identifier=key_identifier).send()
    except News.DoesNotExist:
        pass


def post_month_recap():
    last_month_datetime = timezone.now() + timezone.timedelta(days=-30)
    posts = Post.all_published_post().filter(publish_date__gt=last_month_datetime)
    message = render_to_string(
        "newsletter/email/monthly_posts_recap.html", context={"posts": posts}
    )
    News.objects.create(subject="All posts of the Month", message=message).send()
