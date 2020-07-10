from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Contributor, Project

admin.site.register(Contributor)
admin.site.register(Project, MarkdownxModelAdmin)
