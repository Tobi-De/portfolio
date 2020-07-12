from django.contrib import admin

from .models import Category, Comment, Post, Series

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Series)


@admin.register(Post)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "publish_date", "author", "created"]
    list_filter = ["categories", "status"]
