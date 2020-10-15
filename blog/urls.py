from django.urls import path

from .views import (
    NewPostView,
    PublishPostView,
    PostCreateView,
    PostContentEditorView,
    PostListView,
    PostDetailView,
    SecretKeyPostDetailView,
    PostDeleteView,
    PostUpdateView,
    SeriesListView,
    SeriesCreateView,
    SeriesDetailView,
    SeriesUpdateView,
    SeriesDeleteView,
)

app_name = "blog"
urlpatterns = [
    path("new-post/", NewPostView.as_view(), name="new_post"),
    path("post-publish/<str:slug>/", PublishPostView.as_view(), name="post_publish"),
    path("post-list/", PostListView.as_view(), name="post_list"),
    path("post-create/", PostCreateView.as_view(), name="post_create"),
    path(
        "post-content-editor/<str:slug>/",
        PostContentEditorView.as_view(),
        name="post_content_editor",
    ),
    path(
        "post-detail/<str:slug>/",
        PostDetailView.as_view(),
        name="post_detail",
    ),
    path(
        "post-secret/<str:secret_key>/",
        SecretKeyPostDetailView.as_view(),
        name="secret_post_detail",
    ),
    path(
        "post-update/<str:slug>/",
        PostUpdateView.as_view(),
        name="post_update",
    ),
    path(
        "post-delete/<str:slug>/",
        PostDeleteView.as_view(),
        name="post_delete",
    ),
    path(
        "series-list/",
        SeriesListView.as_view(),
        name="series_list",
    ),
    path(
        "series-create/",
        SeriesCreateView.as_view(),
        name="series_create",
    ),
    path(
        "series-detail/<str:slug>/",
        SeriesDetailView.as_view(),
        name="series_detail",
    ),
    path(
        "series-update/<str:slug>/",
        SeriesUpdateView.as_view(),
        name="series_update",
    ),
    path(
        "series-delete/<str:slug>/",
        SeriesDeleteView.as_view(),
        name="series_delete",
    ),
]
