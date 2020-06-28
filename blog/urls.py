from django.urls import path

from .views import (
    HomeView,
    BlogPostCreateView,
    BlogPostContentEditorView,
    BlogPostListView,
    BlogPostDetailView,
    BlogPostDeleteView,
    BlogPostUpdateView,
    BlogPostSeriesListView,
    BlogPostSeriesCreateView,
    BlogPostSeriesDetailView,
    BlogPostSeriesUpdateView,
    BlogPostSeriesDeleteView,
)

app_name = "blog"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
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
    path(
        "blogpostseries-list/",
        BlogPostSeriesListView.as_view(),
        name="blogpostseries_list",
    ),
    path(
        "blogpostseries-create/",
        BlogPostSeriesCreateView.as_view(),
        name="blogpostseries_create",
    ),
    path(
        "blogpostseries-detail/<str:slug>",
        BlogPostSeriesDetailView.as_view(),
        name="blogpostseries_detail",
    ),
    path(
        "blogpostseries-update/<str:slug>",
        BlogPostSeriesUpdateView.as_view(),
        name="blogpostseries_update",
    ),
    path(
        "blogpostseries-delete/<str:slug>",
        BlogPostSeriesDeleteView.as_view(),
        name="blogpostseries_delete",
    ),
]
