from braces.views import FormValidMessageMixin, SuperuserRequiredMixin
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)

from .forms import ProjectForm, CollaboratorForm
from .models import Project, Collaborator


class ProjectCreateView(FormValidMessageMixin, SuperuserRequiredMixin, CreateView):
    form_class = ProjectForm
    form_valid_message = "Project Created"
    template_name = "projects/project_create.html"


class ProjectUpdateView(FormValidMessageMixin, SuperuserRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_update.html"
    form_valid_message = "Project Updated"


class ProjectListView(ListView):
    model = Project
    context_object_name = "projects"


class ProjectDetailView(DetailView):
    model = Project


class ProjectDeleteView(FormValidMessageMixin, SuperuserRequiredMixin, DeleteView):
    model = Project
    form_valid_message = "Project deleted"

    def get_success_url(self) -> str:
        return reverse("projects:project_list")


class CollaboratorCreateView(FormValidMessageMixin, CreateView):
    form_class = CollaboratorForm
    form_valid_message = "Collaborator Created"
    template_name = "projects/collaborator_create.html"


class CollaboratorListView(ListView):
    model = Collaborator
    context_object_name = "collaborators"


class CollaboratorDetailView(DetailView):
    model = Collaborator


class CollaboratorUpdateView(FormValidMessageMixin, SuperuserRequiredMixin, UpdateView):
    model = Collaborator
    form_class = CollaboratorForm
    template_name = "projects/collaborator_update.html"
    form_valid_message = "collaborator Updated"


class CollaboratorDeleteView(FormValidMessageMixin, SuperuserRequiredMixin, DeleteView):
    model = Collaborator
    form_valid_message = "collaborator deleted"

    def get_success_url(self) -> str:
        return reverse("projects:collaborator_list")
