from braces.views import FormValidMessageMixin, SuperuserRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from .forms import ProjectCreateForm, CollaboratorCreateForm
from .models import Project, Collaborator


class ProjectCreateView(FormValidMessageMixin, SuperuserRequiredMixin, CreateView):
    form_class = ProjectCreateForm
    form_valid_message = "Project Created"
    template_name = "projects/project_create.html"


class ProjectUpdateView(FormValidMessageMixin, SuperuserRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = "projects/project_update.html"
    form_valid_message = "Project Updated"


class ProjectDeleteView(FormValidMessageMixin, SuperuserRequiredMixin, DeleteView):
    model = Project
    template_name = "projects/project_delete.html"
    success_url = "projects/list"


class ProjectListView(ListView):
    model = Project
    context_object_name = "projects"


class ProjectDetailView(DetailView):
    model = Project


class CollaboratorCreateView(FormValidMessageMixin, CreateView):
    form_class = CollaboratorCreateForm
    form_valid_message = "Collaborator Created"
    template_name = "projects/collaborator_create.html"


class CollaboratorListView(ListView):
    model = Collaborator
    context_object_name = "collaborators"


class CollaboratorDetailView(DetailView):
    model = Collaborator
