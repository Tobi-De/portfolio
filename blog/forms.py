from django import forms
from markdownx.fields import MarkdownxFormField

from .models import Post


class BlogPostContentForm(forms.Form):
    body = MarkdownxFormField()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "thumbnail",
            "title",
            "overview",
            "status",
            "reading_time",
            "categories",
            "author",
            "series",
            "featured",
            "scheduled_publish_date",
        ]
