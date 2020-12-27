from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from portfolio.blog import Post


class Command(BaseCommand):
    help = "Populate secret_key of posts."

    def handle(self, *args, **options):
        for post in Post.objects.all():
            if not post.secret_key:
                post.secret_key = get_random_string(length=64)
                post.save()
        print("Post secret keys populated")
