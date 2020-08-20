import re

from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse
from django_extensions.db.fields import ShortUUIDField
from markdownx.models import MarkdownxField
from model_utils.models import TimeStampedModel

User = get_user_model()


class Submission(TimeStampedModel):
    email = models.EmailField()
    uuid = ShortUUIDField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def is_email_valid(self):
        email_pattern = re.compile(r"^([\w\-.]+)@([\w\-.]+)\.([a-zA-Z]{2,5})$")
        return email_pattern.fullmatch(self.email)

    def confirm(self):
        self.confirmed = True
        self.save()

    def get_confirmation_link(self):
        return reverse("submission:subscription_confirm", kwargs={"uuid": self.uuid})


class Mailable(TimeStampedModel):
    subject = models.CharField(max_length=60)
    body = MarkdownxField()

    class Meta:
        abstract = True

    def __str(self):
        return self.subject


class TransactionalMail(Mailable):
    pass


class BulkMail(Mailable):
    dispatch_date = models.DateTimeField()
