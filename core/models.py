from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_q.tasks import Schedule
from model_utils import Choices
from model_utils.models import TimeStampedModel
from model_utils.models import TimeStampedModel, SoftDeletableModel, StatusModel
from sorl.thumbnail import ImageField


class Thumbnail(TimeStampedModel):
    image = ImageField(upload_to="thumbnails")
    source = models.URLField(blank=True, null=True)
    alt = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=["alt"])
    primary = models.BooleanField(default=False)

    def __str__(self):
        return self.alt

    @property
    def url(self):
        return self.image.url


class ToolBox(TimeStampedModel):
    # no inspiration for the name
    # a bunch of informations about me and some usefull method (ex: maintenance methods)
    # I don't know where to put
    THEMES_CHOICES = Choices("monokai", "default", "perldoc")
    maintenance_state = models.BooleanField(default=False)
    code_theme = models.CharField(
        max_length=10, choices=THEMES_CHOICES, default="monokai"
    )
    phone_number = models.CharField(max_length=12, default="+22963588213")
    github = models.URLField(default="https://github.com/Tobi-De")
    telegram = models.URLField(default="https://t.me/Tobi_DE1999")
    twitter = models.URLField(
        default="https://twitter.com/Tobi71110248?ref_src=twsrc%5Etfw"
    )
    linkedIn = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "ToolBox"

    def __str__(self):
        return f"Tobi ToolBox"

    def get_user_links(self):
        return {
            "email": User.objects.all().first().email,
            "github": self.github,
            "telegram": self.telegram,
            "twitter": self.twitter,
            "linkedIn": self.linkedIn,
        }

    @classmethod
    def get_toolbox(cls):
        toolbox = ToolBox.objects.all().first()
        if not toolbox:
            return ToolBox.objects.create()
        else:
            return toolbox

    def set_maintenance_state(self, value):
        self.maintenance_state = value
        self.save()
