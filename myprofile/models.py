from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel


class Profile(TimeStampedModel):
    picture = models.ImageField(default="profile/default.jpg")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, blank=True)
    github_profile = models.URLField()
    linkedIn_profile = models.URLField(blank=True)
