from django.contrib import admin

from .models import Category, Comment, Post, Series

admin.site.register(Comment)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "overview", "reading_time", "publish_date", "author", "created"]
    list_filter = ["categories", "status"]
    search_fields = ["title"]


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "overview", "reading_time", "author", "created"]
    list_filter = ["status"]
    search_fields = ["title"]


@admin.register(Category)
class CatergoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "created"]
