from django.urls import path

from .views import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView, )

app_name = "projects"
urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
    path("project-create/", ProjectCreateView.as_view(), name="project_create"),
    path("project-details/<str:slug>/", ProjectDetailView.as_view(), name="project_detail"),
    path("project-update/<str:slug>/", ProjectUpdateView.as_view(), name="project_update"),
    path("project-delete/<str:slug>/", ProjectDeleteView.as_view(), name="project_delete"),
]
