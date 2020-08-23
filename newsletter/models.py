import re

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models, ProgrammingError, IntegrityError, OperationalError
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_extensions.db.fields import RandomCharField
from django_extensions.db.fields import ShortUUIDField
from django_q.tasks import Chain
from django_q.tasks import async_task, Schedule
from model_utils.models import TimeStampedModel

from .utils import get_current_domain_url

DEFAULT_FROM_EMAIL = getattr(settings, "DEFAULT_FROM_EMAIL", "contact@tobidegnon.com")

User = get_user_model()


class Subscriber(TimeStampedModel):
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
            # TODO write a decent welcome message
            # self.send_welcome_mail()

    @classmethod
    def add_subscriber(cls, email, request):
        sub = Subscriber(email=email)
        sub.save()
        sub.send_confirmation_mail(request=request)

    @classmethod
    def remove_subscriber(cls, sub_obj, title, message, **kwargs):
        subject = "Somebody Unsubscribed"
        _message = f"Email :{sub_obj.email}\nTitle: {title}\nMessage: {message}"
        send_mail(
            subject=subject,
            message=_message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=["contact@tobidegnon.com"],
        )
        sub_obj.delete()

    def get_confirmation_link(self, request):
        return request.build_absolute_uri(
            reverse("newsletter:subscribe_confirm", kwargs={"uuid": self.uuid})
        )

    def get_unsubscribe_link(self, request=None):
        # I could have used build_absolute_url, but this is method
        # is called too much and it is not easy to get 'request' each time
        # i'm going with this approach for now
        if request:
            return request.build_absolute_uri(
                reverse("newsletter:unsubscribe", kwargs={"uuid": self.uuid})
            )
        else:
            return f"{get_current_domain_url()}{reverse('newsletter:unsubscribe', kwargs={'uuid': self.uuid})}"

    def send_welcome_mail(self):
        message = render_to_string("newsletter/email/welcome_message.txt",).format(
            "utf-8"
        )
        async_task(
            send_mail,
            subject="Welcome!",
            message=message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
        )

    def send_confirmation_mail(self, request):
        message = render_to_string(
            "newsletter/email/confirmation_message.txt",
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

    @classmethod
    def emailable_subscribers(cls):
        return Subscriber.objects.filter(confirmed=True)


class News(TimeStampedModel):
    subject = models.CharField(max_length=60)
    message = RichTextUploadingField()
    key_identifier = RandomCharField(length=32)
    dispatch_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "news"

    def __str(self):
        return self.subject

    def get_mail_content(self, subscriber, **kwargs):
        request = kwargs.get("request", None)
        message = strip_tags(
            f"{self.message}\n\nYou can unsubscribe to this newsletter at anytime"
            f" via this link {subscriber.get_unsubscribe_link(request=request)}"
        )
        html_message = (
            f"{self.message}\n\nYou can unsubscribe to this newsletter at anytime"
            f" via this link <a href='{subscriber.get_unsubscribe_link(request=request)}'>Unsubscribe</a>"
        )
        return {
            "subject": self.subject,
            "message": strip_tags(message),
            "from_email": DEFAULT_FROM_EMAIL,
            "recipient_list": [subscriber.email],
            "html_message": html_message,
        }

    def create_scheduled_task(self):
        """schedule task does not work when they need argument, I get mulitple
        erros when I try, so this is how I proceed :
        when dispatch is set, a schedule task that does nothing is created
        we know that the hook receive the entire task as argument, so I create a
        task with a unique name that can identify(via the key_identifier attribute)
        the exact news, then the hook is the one that trigger the execution of
        the send_news method of that news
        """
        try:
            Schedule.objects.create(
                func="newsletter.tasks.placeholder_task",
                name=f"{self.key_identifier}",
                hook="newsletter.tasks.send_news_hook",
                schedule_type=Schedule.ONCE,
                next_run=self.dispatch_date,
            )
        except (ProgrammingError, IntegrityError, OperationalError):
            pass

    def setup(self, **kwargs):
        if self.dispatch_date:
            self.create_scheduled_task()
        else:
            self.send(**kwargs)

    def send(self, **kwargs):
        # TODO update how this work creating chunks of recipient_list list
        chain = Chain(cached=True)
        for sub in Subscriber.emailable_subscribers():
            chain.append(send_mail, **self.get_mail_content(subscriber=sub, **kwargs))
        chain.run()
