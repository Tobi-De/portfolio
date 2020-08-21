from django.urls import path

from .views import (
    SubmissionView,
    SubscriptionConfirmView,
    UnsubscribeView,
    SendNews,
    UnsubscribeConfirmationView,
    SendUnsubscribeLinkView,
)

app_name = "newsletter"
urlpatterns = [
    path("submission/", SubmissionView.as_view(), name="submission"),
    path(
        "subscription-confirm/<str:uuid>/",
        SubscriptionConfirmView.as_view(),
        name="subscription_confirm",
    ),
    path("unsubscribe/<str:uuid>/", UnsubscribeView.as_view(), name="unsubscribe"),
    path(
        "unsubscribe-confirmation/",
        UnsubscribeConfirmationView.as_view(),
        name="unsubscribe_confirmation",
    ),
    path(
        "unsubscribe-test/", SendUnsubscribeLinkView.as_view(), name="unsubscribe_test",
    ),
    path("send-news", SendNews.as_view(), name="send_news"),
]
