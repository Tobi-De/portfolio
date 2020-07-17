from django.urls import path

from .views import HomeView, HireMeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("project-create/", HireMeView.as_view(), name="hire_me"),
]
