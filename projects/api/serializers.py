from rest_framework import serializers

from ..models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        class Meta:
            model = Project
            fields = [
                "title",
                "description",
                "status",
                "what_ive_learned",
                "tech_stack",
                "github_link",
                "web_link",
                "featured",
                "thumbnail",
            ]
