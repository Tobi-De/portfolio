import markdown as md
from django import template
from django.template.defaultfilters import stringfilter, safe

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return safe(
        md.markdown(value, extensions=["pymdownx.extra", "pymdownx.highlight", "pymdownx.magiclink"])
    )
