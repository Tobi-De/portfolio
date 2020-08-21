from django.urls import path

from .views import (
    SubmissionView,
    SubscriptionConfirmView,
    UnsubscribeView,
    SendNews,
    unsubscribe_confirmation,
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
        "unsubscribe/confirmation/",
        unsubscribe_confirmation,
        name="unsubscribe_confirmation",
    ),
    path("send-news", SendNews.as_view(), name="send_news"),
]
