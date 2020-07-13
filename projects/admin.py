from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Contributor, Project

admin.site.register(Contributor)


@admin.register(Project)
class ProjectAdmin(MarkdownxModelAdmin):
    list_display = ["title", "tech_stack", "status", "featured", "author", "owner", "github_link", "created"]
    list_filter = ["status"]
