from .models import Post


def placeholder_task():
    # this task does nothing, it is the hook that is usefull in this
    # case
    pass


def publish_post_hook(task):
    # this method is the hook that triggers the publish method
    # the group here is the slug of the post
    try:
        Post.objects.get(slug=task.group).publish()
    except Post.DoesNotExist:
        pass
