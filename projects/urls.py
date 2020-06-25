from django.urls import path

from .views import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    CollaboratorCreateView,
    CollaboratorUpdateView,
    CollaboratorDeleteView,
    CollaboratorListView,
    CollaboratorDetailView,
)

app_name = "projects"
urlpatterns = [
    path("project-create/", ProjectCreateView.as_view(), name="project_create"),
    path("project-list/", ProjectListView.as_view(), name="project_list"),
    path("project-details/<str:slug>", ProjectDetailView.as_view(), name="project_detail"),
    path("project-update/<str:slug>", ProjectUpdateView.as_view(), name="project_update"),
    path("project-delete/<str:slug>", ProjectDeleteView.as_view(), name="project_delete"),
    path("collaborator-create/", CollaboratorCreateView.as_view(), name="collaborator_create"),
    path("collaborator-list/", CollaboratorListView.as_view(), name="collaborator_list"),
    path(
        "collaborator-detail/<str:slug>",
        CollaboratorDetailView.as_view(),
        name="collaborator_detail",
    ),
    path(
        "collaborator-update/<str:slug>",
        CollaboratorUpdateView.as_view(),
        name="collaborator_update",
    ),
    path(
        "collaborator-delete/<str:slug>",
        CollaboratorDeleteView.as_view(),
        name="collaborator_delete",
    ),
]
