from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import PostSerializer, SeriesSerializer
from ..models import Post, Series


class PostViewSet(ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SeriesViewSet(ReadOnlyModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
