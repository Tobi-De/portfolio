from django import forms
from markdownx.fields import MarkdownxFormField


class BlogPostContentForm(forms.Form):
    body = MarkdownxFormField()
