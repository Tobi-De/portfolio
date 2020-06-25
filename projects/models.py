from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from markdownx.models import MarkdownxField
from model_utils import Choices
from model_utils.fields import MonitorField
from model_utils.models import TimeStampedModel, SoftDeletableModel, StatusModel

User = get_user_model()


class Collaborator(TimeStampedModel):
    full_name = models.CharField(max_length=60)
    slug = AutoSlugField(populate_from="full_name")
    github_link = models.URLField(blank=True)
    contacts = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse("projects:collaborator_detail", kwargs={"slug": self.slug})


class Project(TimeStampedModel, StatusModel, SoftDeletableModel):
    STATUS = Choices("in_development", "deployed")
    thumbnail = models.ImageField(blank=True)
    title = models.CharField(max_length=60)
    description = MarkdownxField()
    slug = AutoSlugField(populate_from=["title"])
    what_ive_learned = MarkdownxField("What I've learned", blank=True)
    github_link = models.URLField("Github repository link", blank=True)
    status_changed = MonitorField(monitor="status")
    deployed_version_link = models.URLField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.CharField(max_length=60)
    collaborators = models.ManyToManyField(Collaborator, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:project_detail", kwargs={"slug": self.slug})
