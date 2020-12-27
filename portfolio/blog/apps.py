from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = "portfolio.blog"

    def ready(self):
        try:
            from portfolio import blog
        except ImportError:
            pass
