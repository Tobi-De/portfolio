from django.conf import settings
from django.contrib.sites.models import Site

DEGUB = getattr(settings, "DEBUG", True)


def get_current_domain():
    if DEGUB:
        return "localhost:0000"
    else:
        return Site.objects.last().domain
