from bootstrap_datepicker_plus import DateTimePickerInput
from ckeditor_uploader.fields import RichTextUploadingFormField
from django import forms

from .models import Post


class BlogPostContentForm(forms.Form):
    body = RichTextUploadingFormField()


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
            "scheduled_publish_date",
        ]
        widgets = {
            "scheduled_publish_date": DateTimePickerInput()
        }
