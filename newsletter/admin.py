from django.contrib import admin

from .models import (
    News,
    Submission,

)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["subject", "body", "dispatch_date", "modified", "created"]
    search_fields = ["subject", "body"]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["email", "uuid", "confirmed", "modified", "created"]
    list_filter = ["confirmed"]
    search_fields = ["email"]
