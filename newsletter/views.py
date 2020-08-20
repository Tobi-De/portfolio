from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import View, FormView, TemplateView

from .forms import SubscriptionForm
from .models import Submission


class SubmissionView(View):
    def post(self, request, *args, **kwargs):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            pass
        return render(request, "newsletter/submission.html", {"email": form.cleaned_data["email"]})


class SubmissionFailView(TemplateView):
    template_name = "newsletter/submission_fail.html"


class SubscriptionConfirmView(View):
    def get(self, request, *args, **kwargs):
        submission = get_object_or_404(Submission, uuid=kwargs["uuid"])
        submission.confirm()
        return render(request, "newsletter/subscription_confirm.html")


class UnsubscribeView(FormView):
    template_name = "newsletter/unsubscribe.html"


class SendMassMails(FormView):
    template_name = "newsletter/mass_mailing.html"
