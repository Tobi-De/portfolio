from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import View, FormView

from .forms import SubscriptionForm
from .models import Submission


class SubmissionView(View):

    def get(self, request, *args, **kwargs):  # noqa
        form = SubscriptionForm()
        context = {
            "form": form,
            "is_valid": False
        }
        return render(request, "newsletter/submission.html", context=context)

    def post(self, request, *args, **kwargs):  # noqa
        form = SubscriptionForm(request.POST)
        context = {
            "is_valid": False
        }
        if form.is_valid():
            Submission.add_subscriber(email=form.cleaned_data["email"])
            context["is_valid"] = True
        form = SubscriptionForm()
        context["form"] = form
        return render(request, "newsletter/submission.html", context=context)


class SubscriptionConfirmView(View):
    def get(self, request, *args, **kwargs):  # noqa
        submission = get_object_or_404(Submission, uuid=kwargs["uuid"])
        submission.confirm()
        return render(request, "newsletter/subscription_confirm.html")


class UnsubscribeView(FormView):
    template_name = "newsletter/unsubscribe.html"


class SendMassMails(FormView):
    template_name = "newsletter/mass_mailing.html"
