from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import NewsSerializer, SubscriberSerializer
from ..models import News, Subscriber


class SubscriberViewSet(ReadOnlyModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class NewsViewSet(ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
