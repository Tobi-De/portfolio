from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from portfolio.blog.api.viewsets import PostViewSet, SeriesViewSet
from portfolio.newsletter.api.viewsets import SubscriberViewSet, NewsViewSet
from portfolio.projects.api.viewsets import ProjectViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("projects", ProjectViewSet)
router.register("posts", PostViewSet)
router.register("series", SeriesViewSet)
router.register("news", NewsViewSet)
router.register("subscribers", SubscriberViewSet)

app_name = "api"
urlpatterns = router.urls
