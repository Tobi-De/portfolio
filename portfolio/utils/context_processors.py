from django.conf import settings
from django.core.cache import cache

from core.models import ToolBox


def settings_context(_request):
    """Settings available by default to the templates context."""
    # Note: we intentionally do NOT expose the entire settings
    # to prevent accidental leaking of sensitive information
    return {"DEBUG": settings.DEBUG}


def tobi_de_toolbox(_request):
    toolbox = cache.get("toolbox")
    if not toolbox:
        toolbox = ToolBox.get_toolbox()
        cache.set("code_theme", toolbox, 60 * 60 * 24)
    return {
        "code_theme_path": f"css/pygments_{toolbox.code_theme}.css",
        **toolbox.get_user_links(),
    }
