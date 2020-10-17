import re

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models, ProgrammingError, IntegrityError, OperationalError
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_extensions.db.fields import RandomCharField
from django_extensions.db.fields import ShortUUIDField
from django_q.tasks import async_task, Schedule, schedule
from markdownx.models import MarkdownxField
from model_utils.models import TimeStampedModel

from core.templatetags.core_tags import markdown
from core.utils import get_current_domain_url

User = get_user_model()


# TODO send a recap of blog posts every month end


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
            self.send_welcome_mail()

    @classmethod
    def add_subscriber(cls, email):
        sub = Subscriber(email=email)
        sub.save()
        sub.send_confirmation_mail()

    @classmethod
    def remove_subscriber(cls, sub_obj, title, message, **kwargs):
        subject = "Somebody Unsubscribed"
        _message = f"Email :{sub_obj.email}\nTitle: {title}\nMessage: {message}"
        send_mail(
            subject=subject,
            message=_message,
            from_email=None,
            recipient_list=["contact@tobidegnon.com"],
        )
        sub_obj.delete()

    def get_confirmation_link(self):
        return f"{get_current_domain_url()}{reverse('newsletter:subscribe_confirm', kwargs={'uuid': self.uuid})}"

    def get_unsubscribe_link(self):
        return f"{get_current_domain_url()}{reverse('newsletter:unsubscribe', kwargs={'uuid': self.uuid})}"

    def send_welcome_mail(self):
        message = render_to_string(
            "newsletter/email/welcome_message.txt",
        ).format("utf-8")
        async_task(
            send_mail,
            subject="Welcome!",
            message=message,
            from_email=None,
            recipient_list=[self.email],
            html_message=render_to_string(
                "newsletter/email/welcome_message.html",
            ),
        )

    def send_confirmation_mail(self):
        message = render_to_string(
            "newsletter/email/confirmation_message.txt",
            context={"link": self.get_confirmation_link()},
        ).format("utf-8")
        async_task(
            send_mail,
            subject="Confirm Email",
            message=message,
            from_email=None,
            recipient_list=[self.email],
            html_message=render_to_string(
                "newsletter/email/confirmation_message.html",
                {"link": self.get_confirmation_link()},
            ),
        )

    # for testing purpose
    def send_unsubscription_link(self):
        subject = "Unsubscribe"
        message = f"Unsubscription link {self.get_unsubscribe_link()}"
        async_task(
            send_mail,
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[self.email],
        )

    @classmethod
    def emailable_subscribers(cls):
        return Subscriber.objects.filter(confirmed=True).order_by("-created")


class News(TimeStampedModel):
    subject = models.CharField(max_length=60)
    message = MarkdownxField()
    key_identifier = RandomCharField(length=32)
    dispatch_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "news"

    def __str(self):
        return self.subject

    def get_mail_content(self, subscriber):
        marked_content = markdown(self.message)
        message = strip_tags(
            f"{marked_content}\n\nYou can unsubscribe to this newsletter at anytime"
            f" via this link {subscriber.get_unsubscribe_link()}."
        )
        html_message = (
            f"{marked_content}\n\nYou can "
            f"<a href='{subscriber.get_unsubscribe_link()}'>unsubscribe</a> to this newsletter at anytime."
        )
        return {
            "subject": self.subject,
            "message": strip_tags(message),
            "from_email": None,
            "recipient_list": [subscriber.email],
            "html_message": html_message,
        }

    def create_scheduled_task(self):
        try:
            schedule(
                func="newsletter.tasks.send_news_task",
                key_identifier=self.key_identifier,
                schedule_type=Schedule.ONCE,
                next_run=self.dispatch_date,
            )
        except (ProgrammingError, IntegrityError, OperationalError):
            pass

    def setup(self):
        if self.dispatch_date:
            self.create_scheduled_task()
        else:
            self.send()

    def send(self):
        if Subscriber.emailable_subscribers().count() == 0:
            return
        self.async_mass_mailing(news_object=self)

    @classmethod
    def async_mass_mailing(cls, news_object, offset=0, limit=100):
        if Subscriber.emailable_subscribers()[offset:].count() <= 0:
            return
        for sub in Subscriber.emailable_subscribers()[offset: offset + limit]:
            send_mail(**news_object.get_mail_content(subscriber=sub))
        async_task(
            News.async_mass_mailing,
            news_object=news_object,
            offset=offset + limit,
            limit=limit,
        )
