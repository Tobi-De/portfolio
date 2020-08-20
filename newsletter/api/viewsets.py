from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import BulkMailSerializer, TransactionalMailSerializer, SubmissionSerializer
from ..models import TransactionalMail, BulkMail, Submission


class SubmissionViewSet(ReadOnlyModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BulkMailViewSet(ReadOnlyModelViewSet):
    queryset = BulkMail.objects.all()
    serializer_class = BulkMailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TransactionalMailViewSet(ReadOnlyModelViewSet):
    queryset = TransactionalMail.objects.all()
    serializer_class = TransactionalMailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
