from django import forms


class SubscriptionForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Enter your email address"}), label="")
