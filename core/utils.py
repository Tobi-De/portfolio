from django.conf import settings
from django.contrib.sites.models import Site

DEGUB = getattr(settings, "DEBUG", True)


def get_current_domain_url():
    if DEGUB:
        return "localhost:8000"
    else:
        return f"https://www.{Site.objects.last().domain}"
