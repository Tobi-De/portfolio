from django import forms
from markdownx.fields import MarkdownxFormField

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "title", "status", "categories", "author", "blogpostseries", "thumbnail"
        ]


class BlogPostContentForm(forms.Form):
    body = MarkdownxFormField()
