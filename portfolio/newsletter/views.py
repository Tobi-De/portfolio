from braces.views import SuperuserRequiredMixin
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, FormView, TemplateView
from django_q.tasks import async_task

from .forms import SubscriptionForm, NewsForm, UnsubscriptionForm, EmailForm
from .models import Subscriber


class SubscriptionView(View):
    def get(self, request, *args, **kwargs):  # noqa
        form = SubscriptionForm()
        context = {"form": form, "is_valid": False}
        return render(request, "newsletter/subscribe.html", context=context)

    def post(self, request, *args, **kwargs):  # noqa
        form = SubscriptionForm(request.POST)
        context = {"is_valid": False}
        if form.is_valid():
            Subscriber.add_subscriber(email=form.cleaned_data["email"])
            context["is_valid"] = True
        form = SubscriptionForm()
        context["form"] = form
        return render(request, "newsletter/subscribe.html", context=context)


class SubscribeConfirmView(View):
    """View called when user click on the confirmation link he received by mail"""

    def get(self, request, *args, **kwargs):  # noqa
        submission = get_object_or_404(Subscriber, uuid=kwargs["uuid"])
        submission.confirm()
        return render(request, "newsletter/subscribe_confirm.html")


class UnsubscribeView(FormView):
    """View called when a user clik on his unsubscribe link"""

    template_name = "newsletter/unsubscribe.html"
    form_class = UnsubscriptionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj"] = get_object_or_404(Subscriber, uuid=self.kwargs.get("uuid"))
        return context

    def form_valid(self, form):
        async_task(
            Subscriber.remove_subscriber,
            sub_obj=self.get_context_data().get("obj"),
            **form.cleaned_data,
        )
        return redirect("newsletter:unsubscribe_confirm")


class UnsubscribeConfirmView(TemplateView):
    template_name = "newsletter/unsubscribe_confirm.html"


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
            sub = Subscriber.objects.create(
                email=form.cleaned_data["email"], confirmed=True
            )
            sub.send_unsubscription_link()
            messages.success(request, "Link Sent")
        return render(
            request, "newsletter/unsubscribe_test.html", context={"form": form}
        )


class SendNews(SuperuserRequiredMixin, FormView):
    template_name = "newsletter/send_news.html"
    form_class = NewsForm

    def form_valid(self, form):
        form.save().setup()
        messages.success(self.request, "Sending...")
        return render(
            self.request, "newsletter/send_news.html", context={"form": NewsForm()}
        )
