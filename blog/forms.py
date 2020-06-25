from django import forms
from markdownx.fields import MarkdownxFormField

from .models import BlogPost, BlogPostSeries


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "thumbnail", "title", "status", "categories", "author", "blogpostseries"
        ]


class BlogPostContentForm(forms.Form):
    body = MarkdownxFormField()


class BlogPostSeriesForm(forms.ModelForm):
    class Meta:
        model = BlogPostSeries
        fields = ["thumbnail", "title", "body", ]

