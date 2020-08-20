from django.urls import path

from .views import home, HireMeView

urlpatterns = [
    path("", home, name="home"),
    path("hire-me/", HireMeView.as_view(), name="hire_me"),
]
