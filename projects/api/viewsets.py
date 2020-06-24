from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .permissions import IsOwnerOrReadOnly
from .serializers import ProjectSerializer, CollaboratorSerializer
from ..models import Project, Collaborator


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CollaboratorViewSet(ModelViewSet):
    queryset = Collaborator.objects.all()
    serializer_class = CollaboratorSerializer
