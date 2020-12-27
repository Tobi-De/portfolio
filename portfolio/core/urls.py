from django.urls import path

from .views import home, GetInTouchView

urlpatterns = [
    path("", home, name="home"),
    path("get-in-touch/", GetInTouchView.as_view(), name="contact_me"),
]
