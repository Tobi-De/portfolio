from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        try:
            import blog.signals
        except ImportError:
            pass
