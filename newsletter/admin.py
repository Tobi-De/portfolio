from django.contrib import admin

from .models import (
    TransactionalMail,
    BulkMail,
    Submission,

)


class MailableAdmin:
    list_display = ["subject", "body", "created"]


@admin.register(TransactionalMail)
class TransactionMailAdmin(admin.ModelAdmin):
    pass


@admin.register(BulkMail)
class BulkMailAdmin(admin.ModelAdmin):
    list_display = MailableAdmin.list_display + ["dispatch_date"]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["email", "uuid", "confirmed", "created"]
    list_filter = ["confirmed"]
    search_fields = ["email"]
