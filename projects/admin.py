from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "tech_stack", "status", "featured", "github_link", "modified", "created"]
    list_filter = ["status", "featured"]
