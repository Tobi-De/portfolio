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
    path("create/", ProjectCreateView.as_view(), name="project_create"),
    path("list/", ProjectListView.as_view(), name="project_list"),
    path("details/<str:slug>", ProjectDetailView.as_view(), name="project_detail"),
    path("update/<str:slug>", ProjectUpdateView.as_view(), name="project_update"),
    path("delete/<str:slug>", ProjectDeleteView.as_view(), name="project_delete"),
    path("create-cb/", CollaboratorCreateView.as_view(), name="collaborator_create"),
    path("list-cb/", CollaboratorListView.as_view(), name="collaborator_list"),
    path(
        "details-cb/<str:slug>",
        CollaboratorDetailView.as_view(),
        name="collaborator_detail",
    ),
    path("update-cb/<str:slug>", CollaboratorUpdateView.as_view(), name="collaborator_update"),
    path("delete-cb/<str:slug>", CollaboratorDeleteView.as_view(), name="collaborator_delete"),
]
