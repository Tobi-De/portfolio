from django.contrib import admin

from .models import Category, Post, Series


class PostableAdmin:
    list_display = ["title", "status", "overview", "reading_time", "author", "created"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = PostableAdmin.list_display + ["publish_date", "created"]
    list_filter = ["categories", "status"]
    search_fields = ["title"]


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = PostableAdmin.list_display + ["reading_time"]
    list_filter = ["status"]
    search_fields = ["title"]


@admin.register(Category)
class CatergoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "created"]
