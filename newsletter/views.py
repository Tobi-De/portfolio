from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, FormView

from .forms import SubscriptionForm, NewsForm, UnsubscriptionReasonForm, EmailForm
from .models import Submission


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
        context["obj"] = get_object_or_404(Submission, uuid=kwargs.get("uuid"))
        return context

    def form_valid(self, form):
        obj = self.get_context_data().get("obj")
        obj.delete()
        return redirect("unsubscribe_confirmation")


def unsubscribe_confirmation(request):
    return render(request, "newsletter/unsubscribe_confirmation.html")


# for testing_purpose
def send_unsubscription_link(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            sub = Submission.objects.create(email=form.cleaned_data["email"], confirmed=True)
            sub.send_unsubscription_link(request=request)
    else:
        form = EmailForm()
    context = {
        "form": form
    }
    return render(request, "newsletter/unsubscribe_test.html", context=context)


class SendNews(FormView):
    template_name = "newsletter/send_news.html"
    form_class = NewsForm
