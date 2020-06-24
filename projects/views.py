from braces.views import FormValidMessageMixin, SuperuserRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .forms import ProjectCreateForm, CollaboratorCreateForm
from .models import Project, Collaborator


class ProjectCreateView(FormValidMessageMixin, SuperuserRequiredMixin, CreateView):
    form_class = ProjectCreateForm
    form_valid_message = "Project Created"
    template_name = "projects/project_create.html"


class ProjectUpdateView(FormValidMessageMixin, SuperuserRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = "projects/project_update.html"
    form_valid_message = "Project Updated"


class ProjectDeleteView(FormValidMessageMixin, SuperuserRequiredMixin, DeleteView):
    model = Project
    form_valid_message = "Project deleted"
    success_url = "/projects/list"


class ProjectListView(ListView):
    model = Project
    context_object_name = "projects"


class ProjectDetailView(DetailView):
    model = Project


class CollaboratorCreateView(FormValidMessageMixin, CreateView):
    form_class = CollaboratorCreateForm
    form_valid_message = "Collaborator Created"
    template_name = "projects/collaborator_create.html"


class CollaboratorUpdateView(FormValidMessageMixin, SuperuserRequiredMixin, UpdateView):
    model = Collaborator
    form_class = CollaboratorCreateForm
    template_name = "projects/collaborator_update.html"
    form_valid_message = "collaborator Updated"


class CollaboratorDeleteView(FormValidMessageMixin, SuperuserRequiredMixin, DeleteView):
    model = Collaborator
    form_valid_message = "collaborator deleted"
    success_url = "/collaborators/list-cb"


class CollaboratorListView(ListView):
    model = Collaborator
    context_object_name = "collaborators"


class CollaboratorDetailView(DetailView):
    model = Collaborator
