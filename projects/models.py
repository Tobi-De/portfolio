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

# TODO Add these as base in a migration
STACK_CHOICES = Choices(
    "django_vuejs_html_css_bootstrap4",
    "django_vuejs_html_css_bulma",
    "django_html_css_bootstrap4",
    "django_html_css_bulma",
    "vuejs_html_css_bootstrap4",
    "vuejs_html_css_bulma",
    "wagtail_html_css_bootstrap4",
    "wagtail_html_css_vuejs",
)


# from pygments.lexers import get_all_lexers
# from pygments.styles import get_all_styles
#
# LEXERS = [item for item in get_all_lexers() if item[1]]
# LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
# STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])
#
#
# class Snippet(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     title = models.CharField(max_length=100, blank=True, default='')
#     code = models.TextField()
#     linenos = models.BooleanField(default=False)
#     language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
#     style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
#
#     class Meta:
#         ordering = ['created']


class Technology(TimeStampedModel):
    name = models.CharField(unique=True, db_index=True, max_length=100)
    link = models.URLField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.name


# TODO add way to showcase code snippets
# TODO try so seee if those snippets can be used directy in the blog post(tempplate tags)
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
