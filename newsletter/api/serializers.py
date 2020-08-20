from rest_framework import serializers

from ..models import TransactionalMail, Submission, BulkMail


class BulkMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkMail
        fields = "__all__"


class TransactionalMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionalMail
        fields = "__all__"


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"
