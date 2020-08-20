from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from markdownx.models import MarkdownxField
from model_utils import Choices
from model_utils.fields import MonitorField
from model_utils.models import TimeStampedModel, SoftDeletableModel, StatusModel

User = get_user_model()


class Project(TimeStampedModel, StatusModel, SoftDeletableModel):
    STACK_CHOICES = Choices("django_vuejs", "django", "vuejs", "wagtail", "wagtail_vuejs")
    STATUS = Choices("in_development", "deployed")
    thumbnail = models.ImageField(blank=True)
    title = models.CharField(max_length=60)
    description = models.TextField()
    slug = AutoSlugField(populate_from=["title"])
    tech_stack = models.CharField(max_length=20, choices=STACK_CHOICES, default=STACK_CHOICES.django)
    featured = models.BooleanField(default=False)
    what_ive_learned = MarkdownxField("What I've learned", blank=True)
    github_link = models.URLField("Github repository link", blank=True)
    status_changed = MonitorField(monitor="status")
    web_link = models.URLField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:project_detail", kwargs={"slug": self.slug})

    @property
    def get_stack(self):
        return self.tech_stack.split("_")
