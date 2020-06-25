from django.urls import path

from .views import (
    BlogPostCreateView,
    BlogPostContentEditorView,
    BlogPostListView,
    BlogPostDetailView,
    BlogPostDeleteView,
    BlogPostUpdateView,
)

app_name = "blog"
urlpatterns = [
    path("blogpost-list/", BlogPostListView.as_view(), name="blogpost_list"),
    path("blogpost-create/", BlogPostCreateView.as_view(), name="blogpost_create"),
    path(
        "blogpost-content-editor/<str:slug>",
        BlogPostContentEditorView.as_view(),
        name="blogpost_content_editor",
    ),
    path(
        "blogpost-detail/<str:slug>",
        BlogPostDetailView.as_view(),
        name="blogpost_detail",
    ),
    path(
        "blogpost-update/<str:slug>",
        BlogPostUpdateView.as_view(),
        name="blogpost_update",
    ),
    path(
        "blogpost-delete/<str:slug>",
        BlogPostDeleteView.as_view(),
        name="blogpost_delete",
    ),
]
