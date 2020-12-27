from django.contrib import admin

from .models import Project, Technology


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ["name", "link", "created"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "featured", "github_link", "modified", "created"]
    list_filter = ["status", "featured"]
    search_fields = ["title"]
