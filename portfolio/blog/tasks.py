from .models import Post


def publish_post_task(slug):
    try:
        Post.objects.get(slug=slug).publish()
    except Post.DoesNotExist:
        pass
