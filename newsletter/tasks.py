from blog.models import Post
from .models import News


def send_news_task(key_identifier):
    try:
        News.objects.get(key_identifier=key_identifier).send()
    except News.DoesNotExist:
        pass


def post_month_recap():
    # filter by last month post
    posts = Post.all_published_post()
    # read message template
    # create news and send it
