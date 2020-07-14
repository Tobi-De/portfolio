from django.contrib import admin

from .models import (
    TransactionalMail,
    BulkMail,
    Newsletter,
    Submission,
    SimpleMessage,
    TemplateMessage,
)


class MessageableAdminMixin(admin.ModelAdmin):
    list_display = ["subject", "body", "tags", "created"]
    list_filter = ["tags"]
    search_fields = ["subject", "body"]


@admin.register(SimpleMessage)
class SimpleMessageAdmin(MessageableAdminMixin):
    pass


@admin.register(TemplateMessage)
class TemplateMessageAdmin(MessageableAdminMixin):
    pass


class MailableAdminMixin(admin.ModelAdmin):
    list_display = ["message", "dispatch_date", "newsletter", "created"]


@admin.register(TransactionalMail)
class TransactionMailAdmin(MailableAdminMixin):
    pass


@admin.register(BulkMail)
class BulkMailAdmin(MailableAdminMixin):
    pass


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "slug", "created"]
    search_fields = ["title"]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["email", "uuid", "confirmed", "created"]
    list_filter = ["confirmed"]
    search_fields = ["email"]
