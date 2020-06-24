from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from projects.api.viewsets import ProjectViewSet, CollaboratorViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("projects", ProjectViewSet)
router.register("collaborators", CollaboratorViewSet)

app_name = "api"
urlpatterns = router.urls
