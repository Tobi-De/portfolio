from django.contrib import admin
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from sorl.thumbnail.admin import AdminImageMixin

from .models import Profile, Thumbnail, Maintenance


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    pass


class ThumbnailLinkMixin:

    def thumbnail_link(self, obj):
        url = reverse("admin:core_thumbnail_change", args=[obj.thumbnail.id])
        link = '<a href="%s">%s</a>' % (url, obj.thumbnail.alt)
        return mark_safe(link)

    thumbnail_link.short_description = "thumbnail"


@admin.register(Thumbnail)
class ThumbnailAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ["slug", "image", "source", "alt", "created", "modified"]
    list_filter = ["primary"]


@admin.register(Profile)
class ProfileAdmin(ThumbnailLinkMixin, admin.ModelAdmin):
    list_display = ["user", "github_profile", "modified", "created"]
