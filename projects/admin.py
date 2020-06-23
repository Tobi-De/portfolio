from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Collaborator, Project

admin.site.register(Collaborator)
admin.site.register(Project, MarkdownxModelAdmin)
