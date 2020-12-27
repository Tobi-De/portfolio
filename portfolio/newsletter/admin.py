from django.contrib import admin

from .models import News, Subscriber


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["subject", "key_identifier", "dispatch_date", "modified", "created"]
    search_fields = ["subject", "message"]


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "uuid", "confirmed", "modified", "created"]
    list_filter = ["confirmed"]
    search_fields = ["email"]
