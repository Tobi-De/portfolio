from .models import News


def send_news_task(key_identifier):
    try:
        News.objects.get(key_identifier=key_identifier).send()
    except News.DoesNotExist:
        pass
