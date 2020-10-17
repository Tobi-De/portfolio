from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django_extensions.db.fields import AutoSlugField
from markdownx.models import MarkdownxField
from model_utils import Choices
from model_utils.fields import MonitorField
from model_utils.models import TimeStampedModel, SoftDeletableModel, StatusModel

User = get_user_model()


class Technology(TimeStampedModel):
    name = models.CharField(unique=True, db_index=True, max_length=100)
    link = models.URLField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.name


class Project(TimeStampedModel, StatusModel, SoftDeletableModel):
    STATUS = Choices("in_development", "deployed")
    carousel = models.ManyToManyField("core.Thumbnail", blank=True)
    title = models.CharField(max_length=60)
    description = MarkdownxField()
    slug = AutoSlugField(populate_from=["title"])
    tech_stack = models.ManyToManyField(Technology)
    featured = models.BooleanField(default=False)
    what_ive_learned = MarkdownxField()
    github_link = models.URLField("Github repository link", blank=True)
    status_changed = MonitorField(monitor="status")
    web_link = models.URLField(blank=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:project_detail", kwargs={"slug": self.slug})

    @property
    def get_status(self):
        return self.status.replace("_", " ").capitalize()

    @property
    def overview(self):
        return strip_tags(self.description[:85]) + "..."

    @property
    def primary_image(self):
        image = self.carousel.filter(primary=True).first()
        return image if image else self.carousel.all().first()
