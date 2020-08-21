import re

import environ
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django_extensions.db.fields import ShortUUIDField
from django_q.tasks import async_task
from markdownx.models import MarkdownxField
from model_utils.models import TimeStampedModel, SoftDeletableModel

env = environ.Env()

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="contact@tobidegnon.com")

User = get_user_model()


class Submission(TimeStampedModel, SoftDeletableModel):
    email = models.EmailField(unique=True)
    uuid = ShortUUIDField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def is_email_valid(self):
        email_pattern = re.compile(r"^([\w\-.]+)@([\w\-.]+)\.([a-zA-Z]{2,5})$")
        return email_pattern.fullmatch(self.email)

    def confirm(self):
        if not self.confirmed:
            self.confirmed = True
            self.save()
            self.send_welcome_mail()

    @classmethod
    def add_subscriber(cls, email, request):
        sub = Submission(email=email)
        sub.save()
        sub.send_confirmation_mail(request=request)

    def get_confirmation_link(self, request):
        return request.build_absolute_uri(
            reverse("newsletter:subscription_confirm", kwargs={"uuid": self.uuid})
        )

    def get_unsubscribe_link(self, request):
        return request.build_absolute_uri(
            reverse("newsletter:unsubscribe", kwargs={"uuid": self.uuid})
        )

    def send_welcome_mail(self):
        message = render_to_string("newsletter/messages/welcome_email.txt", ).format(
            "utf-8"
        )
        async_task(
            send_mail,
            subject="Welcome to my Newsletter",
            message=message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
        )

    def send_confirmation_mail(self, request):
        message = render_to_string(
            "newsletter/messages/confirmation_email.txt",
            {"link": self.get_confirmation_link(request=request)},
        ).format("utf-8")
        async_task(
            send_mail,
            subject="Confirm Email",
            message=message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
        )

    # for testing purpose
    def send_unsubscription_link(self, request):
        subject = "Unsubscribe"
        message = f"Unsubscription link {self.get_unsubscribe_link(request=request)}"
        async_task(
            send_mail,
            subject=subject,
            message=message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
        )


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


class UnsubscriptionReason(TimeStampedModel):
    pass
