from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from core.admin import ThumbnailLinkMixin
from .models import Category, Post, Series


class PostableAdmin(ThumbnailLinkMixin, MarkdownxModelAdmin):
    list_display = [
        "title",
        "thumbnail_link",
        "status",
        "overview",
        "reading_time",
        "created",
    ]


@admin.register(Post)
class PostAdmin(PostableAdmin, admin.ModelAdmin):
    list_display = PostableAdmin.list_display + ["publish_date", "created"]
    list_filter = ["categories", "status"]
    search_fields = ["title"]


@admin.register(Series)
class SeriesAdmin(PostableAdmin, admin.ModelAdmin):
    list_display = PostableAdmin.list_display + ["reading_time"]
    list_filter = ["status"]
    search_fields = ["title"]


@admin.register(Category)
class CatergoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "created"]
