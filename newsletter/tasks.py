from .models import News


def placeholder_task():
    # this task does nothing, it is the hook that is usefull in this
    # case
    pass


def send_news_hook(task):
    # this method is the hook that triggers the send_news method
    # the group here is the key_identifier of the news
    try:
        News.objects.get(key_identifier=task.group).send()
    except News.DoesNotExist:
        pass
