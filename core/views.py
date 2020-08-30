from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import FormView
from django_q.tasks import async_task

from projects.models import Project
from .forms import ContactMeForm
from .models import Profile

DEFAULT_FROM_EMAIL = getattr(settings, "DEFAULT_FROM_EMAIL", "contact@tobidegnon.com")


def home(request):
    featured = Project.objects.filter(featured=True).order_by("-created")[:3]
    profile = Profile.objects.last()
    context = {"featured": featured, "profile": profile}
    return render(request, "core/home.html", context)


# TODO write a telegram bot that send message whenever a message is sent
class ContactMeView(FormView):
    form_class = ContactMeForm
    template_name = "core/contact_me.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.last()
        return context

    def form_valid(self, form):
        message = (
            f"Full Name: {form.cleaned_data['full_name']}\n"
            f"Email: {form.cleaned_data['email']}\n\n"
            f"{form.cleaned_data['message']}"
        )
        async_task(
            send_mail,
            subject=form.cleaned_data["subject"],
            message=message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[
                "contact@tobidegnon.com",
                "tobidegnon@protonmail.com",
                "degnonfrancis@gmail.com",
            ],
        )
        messages.success(
            self.request, "Thanks for your message, I will be reaching to you soon !"
        )

        return render(self.request, "core/contact_me.html", {"form": ContactMeForm()})
