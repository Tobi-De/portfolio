from django import forms
from markdownx.fields import MarkdownxFormField

from .models import Post, Series


class BlogPostContentForm(forms.Form):
    body = MarkdownxFormField(label="")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "thumbnail",
            "title",
            "overview",
            "status",
            "tags",
            "series",
            "featured",
            "scheduled_publish_date",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["overview"].label = ""


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ["thumbnail", "title", "overview", "body", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["overview"].label = ""
        self.fields["body"].label = ""
