from django import forms


class GetInTouchForm(forms.Form):
    full_name = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={"placeholder": "last name first name"}),
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"placeholder": "a valid email address so I can respond back"}
        )
    )
    subject = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"placeholder": "the reason why you are trying to reach out"}
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "want to get a job done ? or need an answer "
                "to a question ? ask me anything :)"
            }
        )
    )
