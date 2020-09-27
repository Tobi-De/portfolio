from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import Post


class LatestPostsFeed(Feed):
    feed_type = Atom1Feed
    title = "Tobi-De Blog Posts"
    link = ""
    description = "Updates on new posts on Tobi-De personal Blog."
    author_link = "www.tobidegnon.com"
    author_email = "degnonfrancis@gmail.com"

    def items(self):  # noqa
        return Post.objects.filter(status=Post.STATUS.published).order_by("-created")

    def item_title(self, item):
        return item.title  # noqa

    def item_description(self, item):
        return item.overview  # noqa
