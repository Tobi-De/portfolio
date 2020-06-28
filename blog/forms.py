from django import forms
from markdownx.fields import MarkdownxFormField

from .models import Comment


class BlogPostContentForm(forms.Form):
    body = MarkdownxFormField()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["user_name", "content"]
