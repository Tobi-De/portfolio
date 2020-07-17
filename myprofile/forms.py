from django import forms


class HireMeForm(forms.Form):
    full_name = forms.CharField(label="Your full name(required)", max_length=60)
    email = forms.EmailField(label="Your Email(required)")
    subject = forms.CharField(label="Subject(required)", max_length=30)
    message = forms.CharField(label="Message(required)", widget=forms.Textarea)
