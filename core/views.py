from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import FormView
from django_q.tasks import async_task

from projects.models import Project
from .forms import GetInTouchForm
from .models import ToolBox

DEFAULT_FROM_EMAIL = getattr(settings, "DEFAULT_FROM_EMAIL", "contact@tobidegnon.com")


def home(request):
    featured = Project.objects.filter(featured=True).order_by("-priority", "-created")[
        :3
    ]
    context = {"featured": featured, **ToolBox.get_toolbox().user_links}
    return render(request, "core/home.html", context)


# TODO write a telegram bot that send message whenever a message is sent
class GetInTouchView(FormView):
    form_class = GetInTouchForm
    template_name = "core/get_in_touch.html"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            **ToolBox.get_toolbox().user_links,
        }

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
                "tobidegnon@protonmail.com",
                "degnonfrancis@gmail.com",
            ],
        )
        messages.success(
            self.request, "Thanks for your message, I will be reaching you soon !"
        )

        return render(
            self.request, "core/get_in_touch.html", {"form": GetInTouchForm()}
        )
