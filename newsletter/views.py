from django.shortcuts import render
from django.views.generic import View, FormView


class SubmissionView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "newsletter/submission.html")


class SubscriptionConfirmView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "newsletter/subscription_confirm.html")


class UnsubscribeView(FormView):
    template_name = "newsletter/unsubscribe.html"


class SendMassMails(FormView):
    template_name = "newsletter/mass_mailing.html"
