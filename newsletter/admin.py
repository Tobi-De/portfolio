from django.contrib import admin

from .models import (
    TransactionalMail,
    BulkMail,
    Submission,

)


class MailableAdminMixin(admin.ModelAdmin):
    list_display = ["subject", "body", "created"]


@admin.register(TransactionalMail)
class TransactionMailAdmin(MailableAdminMixin):
    pass


@admin.register(BulkMail)
class BulkMailAdmin(MailableAdminMixin):
    list_display = MailableAdminMixin.list_display + ["dispatch_date"]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["email", "uuid", "confirmed", "created"]
    list_filter = ["confirmed"]
    search_fields = ["email"]
