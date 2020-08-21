from django import forms

from .models import Submission


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "Enter your email address"
        self.fields["email"].label = ""


class NewsForm(forms.Form):
    subject = forms.CharField(max_length=130)
