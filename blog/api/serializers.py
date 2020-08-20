from rest_framework import serializers

from ..models import Post, Series, Category


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
