from django.contrib import admin
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from markdownx.admin import MarkdownxModelAdmin

from portfolio.core.admin import ThumbnailLinkMixin
from .models import Post, Series


class PostableAdmin(ThumbnailLinkMixin, MarkdownxModelAdmin):
    list_display = [
        "title",
        "thumbnail_link",
        "status",
        "reading_time",
        "created",
    ]


@admin.register(Post)
class PostAdmin(PostableAdmin, admin.ModelAdmin):
    list_display = PostableAdmin.list_display + ["publish_date", "series_link"]
    list_filter = ["status"]
    search_fields = ["title"]

    def series_link(self, obj):
        try:
            _id = obj.series.id
        except AttributeError:
            return None
        else:
            url = reverse("admin:blog_series_change", args=[_id])
            link = '<a href="%s">%s</a>' % (url, obj.series.title)
            return mark_safe(link)

    series_link.short_description = "series"


@admin.register(Series)
class SeriesAdmin(PostableAdmin, admin.ModelAdmin):
    list_display = PostableAdmin.list_display + ["reading_time"]
    list_filter = ["status", "visible"]
    search_fields = ["title"]
