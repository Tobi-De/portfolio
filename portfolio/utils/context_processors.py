from django.conf import settings

from core.models import ToolBox


def settings_context(_request):
    """Settings available by default to the templates context."""
    # Note: we intentionally do NOT expose the entire settings
    # to prevent accidental leaking of sensitive information
    return {"DEBUG": settings.DEBUG}


def code_theme(_request):
    theme = ToolBox.get_toolbox().code_theme
    return {"code_theme_path": f"css/pygments_{theme}.css"}
