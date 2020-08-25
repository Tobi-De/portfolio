from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_q.tasks import Schedule
from model_utils.models import TimeStampedModel
from model_utils.models import TimeStampedModel, SoftDeletableModel, StatusModel
from sorl.thumbnail import ImageField


class Thumbnail(TimeStampedModel):
    image = ImageField(upload_to="thumbnails")
    source = models.URLField(blank=True, null=True)
    alt = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=["alt"])

    def __str__(self):
        return self.alt

    @property
    def url(self):
        return self.image.url


# TODO add twitter profile
class Profile(TimeStampedModel):
    picture = models.OneToOneField(
        "core.Thumbnail", blank=True, null=True, on_delete=models.SET_NULL
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, blank=True)
    github_profile = models.URLField()
    linkedIn_profile = models.URLField(blank=True)

    def __str__(self):
        return self.user.username
