from django.urls import path

from .views import (
    SubscriptionView,
    SubscribeConfirmView,
    UnsubscribeView,
    SendNews,
    UnsubscribeConfirmView,
    SendUnsubscribeLinkView,
)

app_name = "newsletter"
urlpatterns = [
    path("subscribe/", SubscriptionView.as_view(), name="subscribe"),
    path(
        "subscribe-confirm/<str:uuid>/",
        SubscribeConfirmView.as_view(),
        name="subscribe_confirm",
    ),
    path("unsubscribe/<str:uuid>/", UnsubscribeView.as_view(), name="unsubscribe"),
    path(
        "unsubscribe-confirm/",
        UnsubscribeConfirmView.as_view(),
        name="unsubscribe_confirm",
    ),
    path(
        "unsubscribe-test/", SendUnsubscribeLinkView.as_view(), name="unsubscribe_test",
    ),
    path("send-news/", SendNews.as_view(), name="send_news"),
]
