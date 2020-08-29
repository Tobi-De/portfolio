from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "carousel",
            "title",
            "description",
            "status",
            "what_ive_learned",
            "tech_stack",
            "featured",
            "github_link",
            "web_link",
        ]
