from django.contrib import admin

from .models import Category, Comment, BlogPost, BlogPostSeries

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(BlogPostSeries)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "publish_date", "author", "created"]
    list_filter = ["categories", "status"]
