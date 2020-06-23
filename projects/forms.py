from django import forms

from .models import Project, Collaborator


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "what_ive_learned",
            "github_link",
            "deployed_version_link",
            "author",
            "thumbnail",
        ]


class CollaboratorCreateForm(forms.ModelForm):
    class Meta:
        model = Collaborator
        fields = ["full_name", "github_link", "contacts"]
