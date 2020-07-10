from rest_framework import serializers

from ..models import Contributor, Project


class ProjectSerializer(serializers.ModelSerializer):
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
        model = Contributor
        fields = ["full_name", "github_link", "contacts"]
