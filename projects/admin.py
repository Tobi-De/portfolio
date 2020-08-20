from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Project


@admin.register(Project)
class ProjectAdmin(MarkdownxModelAdmin):
    list_display = ["title", "tech_stack", "status", "featured", "github_link", "modified", "created"]
    list_filter = ["status", "featured"]
