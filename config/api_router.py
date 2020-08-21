from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from blog.api.viewsets import PostViewSet, SeriesViewSet, CategoryViewSet
from newsletter.api.viewsets import (
    SubmissionViewSet,
    NewsViewSet
)
from projects.api.viewsets import ProjectViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("projects", ProjectViewSet)
router.register("posts", PostViewSet)
router.register("series", SeriesViewSet)
router.register("categories", CategoryViewSet)
router.register("news", NewsViewSet)
router.register("submissions", SubmissionViewSet)

app_name = "api"
urlpatterns = router.urls
