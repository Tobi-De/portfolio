from django import forms


class ContactMeForm(forms.Form):
    full_name = forms.CharField(max_length=60)
    email = forms.EmailField()
    subject = forms.CharField(max_length=30)
    message = forms.CharField(widget=forms.Textarea)
