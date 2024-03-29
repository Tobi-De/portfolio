from django import forms

from .models import Subscriber, News


# TODO this form I beleive is used only fo testing purpose, remove it after writing test
class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Enter your email address"}),
        label="",
    )


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "Enter your email address"
        self.fields["email"].label = ""


class UnsubscriptionForm(forms.Form):
    title = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"placeholder": "Short title to describe your reason"}
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Please explain here in few lines why you are leaving us."
            }
        ),
        required=False,
    )


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["message"].label = ""
