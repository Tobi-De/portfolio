from django.urls import path

from .views import home, ContactMeView

urlpatterns = [
    path("", home, name="home"),
    path("contact-me/", ContactMeView.as_view(), name="contact_me"),
]
