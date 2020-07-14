from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse
from django_extensions.db.fields import AutoSlugField, ShortUUIDField
from model_utils.models import TimeStampedModel

User = get_user_model()


class Messageable(TimeStampedModel):
    TAGS_LIST = ["@username"]
    subject = models.CharField(max_length=60)
    body = models.TextField()
    tags = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.subject


class SimpleMessage(Messageable):
    pass


class TemplateMessage(Messageable):
    template_name = models.CharField(max_length=30)


class Mailable(TimeStampedModel):
    message = models.OneToOneField(SimpleMessage, on_delete=models.CASCADE, blank=True, null=True)
    template = models.ManyToManyField(TemplateMessage, blank=True)
    dispatch_date = models.DateTimeField(blank=True, null=True)
    newsletter = models.OneToOneField("Newsletter", on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str(self):
        return self.message


class TransactionalMail(Mailable):
    pass


class BulkMail(Mailable):
    dispatch_date = models.DateTimeField()


class Newsletter(TimeStampedModel):
    title = models.CharField(max_length=60)
    slug = AutoSlugField(populate_from=["title"])
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.title

    def process_mail(self):
        pass

    def process_transactional_mail(self):
        pass

    def process_bulk_mail(self):
        pass


class Submission(TimeStampedModel):
    email = models.EmailField()
    uuid = ShortUUIDField()
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def verifiy_email(self):
        pass

    def get_confirmation_link(self):
        return reverse("newsletter:subscription_confirm", kwargs={"uuid": self.uuid})
