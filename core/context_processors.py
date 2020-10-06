from django.core.cache import cache

from .models import ToolBox


def code_theme(request):
    theme = cache.get("code_theme")
    if not theme:
        theme = ToolBox.get_toolbox().code_theme
        cache.set("code_theme", theme, 60 * 60 * 12)
    return {
        "code_theme_path": f"css/pygments_{theme}.css"
    }
