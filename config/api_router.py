from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from blog.api.viewsets import PostViewSet, SeriesViewSet, CategoryViewSet
from projects.api.viewsets import ProjectViewSet
from newsletter.api.viewsets import (
    SubmissionViewSet,
    TransactionalMailViewSet,
    BulkMailViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("projects", ProjectViewSet)
router.register("posts", PostViewSet)
router.register("series", SeriesViewSet)
router.register("categories", CategoryViewSet)
router.register("bulkmails", BulkMailViewSet)
router.register("transactionalmails", TransactionalMailViewSet)
router.register("submissions", SubmissionViewSet)

app_name = "api"
urlpatterns = router.urls
