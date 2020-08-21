from django import forms

from .models import Submission, UnsubscriptionReason


# For testing purpose


class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Enter your email address"}),
        label="",
    )


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


class UnsubscriptionReasonForm(forms.ModelForm):
    class Meta:
        model = UnsubscriptionReason
        fields = "__all__"

    def __int__(self, *args, **kwargs):
        super().__int__(*args, **kwargs)
        self.fields["message"].widget.attrs[
            "placeholder"
        ] = "Please explain here in few lines why you are leaving us."
