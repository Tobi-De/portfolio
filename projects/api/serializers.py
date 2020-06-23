from rest_framework import serializers

from ..models import Collaborator, Project


class ProjectSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(max_length=60)

    class Meta:
        class Meta:
            model = Project
            fields = [
                "title",
                "description",
                "what_ive_learned",
                "github_link",
                "deployed_version_link",
                "thumbnail",
            ]


class CollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaborator
        fields = ["full_name", "github_link", "contacts"]
