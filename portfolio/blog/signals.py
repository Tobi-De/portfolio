from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post


@receiver(post_save, sender=Post)
def update_series_visibility(sender, instance=None, created=False, **kwargs):
    try:
        post_count = instance.series.published_post().count()
    except Exception:
        pass
    else:
        if post_count >= 2:
            instance.series.visible = True
            instance.series.save()
