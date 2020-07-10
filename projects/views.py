from braces.views import FormValidMessageMixin, SuperuserRequiredMixin
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)

from .forms import ProjectForm
from .models import Project


class ProjectListView(ListView):
    model = Project
    ordering = ["-created"]
    paginate_by = 6
    context_object_name = "projects"


class ProjectDetailView(DetailView):
    model = Project


class ProjectCreateView(FormValidMessageMixin, SuperuserRequiredMixin, CreateView):
    form_class = ProjectForm
    form_valid_message = "Project Created"
    template_name = "projects/project_create.html"


class ProjectUpdateView(FormValidMessageMixin, SuperuserRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_update.html"
    form_valid_message = "Project Updated"


class ProjectDeleteView(FormValidMessageMixin, SuperuserRequiredMixin, DeleteView):
    model = Project
    form_valid_message = "Project deleted"

    def get_success_url(self) -> str:
        return reverse("projects:project_list")
