from django.shortcuts import render
from django.views.generic import FormView

from projects.models import Project
from .forms import HireMeForm


def home(request):
    context = {
        "projects": Project.objects.filter(featured=True).order_by("-created")
    }
    return render(request, "core/home.html", context)


class HireMeView(FormView):
    form_class = HireMeForm
    template_name = "core/hire_me.html"
