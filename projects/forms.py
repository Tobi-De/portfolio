from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "what_ive_learned",
            "github_link",
            "deployed_version_link",
            "author",
            "contributors",
            "thumbnail",
        ]
