from braces.views import SuperuserRequiredMixin
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, FormView, TemplateView

from .forms import SubscriptionForm, NewsForm, UnsubscriptionReasonForm, EmailForm
from .models import Submission
from django_q.tasks import async_task


class SubmissionView(View):
    def get(self, request, *args, **kwargs):  # noqa
        form = SubscriptionForm()
        context = {"form": form, "is_valid": False}
        return render(request, "newsletter/submission.html", context=context)

    def post(self, request, *args, **kwargs):  # noqa
        form = SubscriptionForm(request.POST)
        context = {"is_valid": False}
        if form.is_valid():
            print("here")
            Submission.add_subscriber(email=form.cleaned_data["email"], request=request)
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
    form_class = UnsubscriptionReasonForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj"] = get_object_or_404(Submission, uuid=self.kwargs.get("uuid"))
        return context

    def form_valid(self, form):
        async_task(
            Submission.remove_subscriber,
            sub_obj=self.get_context_data().get("obj"),
            message=form.cleaned_data["message"],
        )
        return redirect("newsletter:unsubscribe_confirmation")


class UnsubscribeConfirmationView(TemplateView):
    template_name = "newsletter/unsubscribe_confirmation.html"


class SendUnsubscribeLinkView(SuperuserRequiredMixin, View):
    """THis views is only for testing purpose, test if the unbubscribe link
        is really sent
    """

    def get(self, request, *args, **kwargs):  # noqa
        return render(
            request, "newsletter/unsubscribe_test.html", context={"form": EmailForm()}
        )

    def post(self, request, *args, **kwargs):  # noqa
        form = EmailForm(request.POST)
        if form.is_valid():
            sub = Submission.objects.create(
                email=form.cleaned_data["email"], confirmed=True
            )
            sub.send_unsubscription_link(request=request)
            messages.success(request, "Link Sent")
        return render(
            request, "newsletter/unsubscribe_test.html", context={"form": form}
        )


class SendNews(FormView):
    template_name = "newsletter/send_news.html"
    form_class = NewsForm
