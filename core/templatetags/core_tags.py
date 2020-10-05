import markdown as md
from django import template
from django.template.defaultfilters import stringfilter, safe

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return safe(
        md.markdown(
            value,
            extensions=[
                "pymdownx.extra",
                "pymdownx.highlight",
                "pymdownx.magiclink",
                "pymdownx.emoji",
                "pymdownx.progressbar",
                "pymdownx.details",
                "pymdownx.critic",
                "pymdownx.inlinehilite",
                "pymdownx.keys",
                "pymdownx.tasklist",
            ],
            options={
                "repo_url_shorthand": True,
                "social_url_shorthand": True,
                "social_url_shortener": True,
                "repo_url_shortener": True,
                "provider": "github",
            },
        )
    )
