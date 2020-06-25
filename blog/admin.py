from django.contrib import admin

from .models import Category, Comment, BlogPost, BlogPostSeries

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(BlogPost)
admin.site.register(BlogPostSeries)
