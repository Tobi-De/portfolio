from django.shortcuts import render
from django.views.generic import View, FormView

from projects.models import Project
from .forms import HireMeForm


class HomeView(View):
    def get(self, request, *ars, **kwargs):
        context = {
            "projects": Project.objects.filter(featured=True).order_by("-created")
        }
        return render(request, "myprofile/home.html", context)


class HireMeView(FormView):
    form_class = HireMeForm
    template_name = "myprofile/hire_me.html"
