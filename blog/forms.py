from django import forms
from markdownx.fields import MarkdownxFormField

from .models import Comment


class BlogPostContentForm(forms.Form):
    body = MarkdownxFormField()


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4'
    }))

    class Meta:
        model = Comment
        fields = ["user_name", "content"]
