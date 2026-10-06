from django.urls import path

from .views import (
    ExchangeListCreateView,
    ExchangeStatusView,
)


urlpatterns = [

    path(
        "",
        ExchangeListCreateView.as_view(),
        name="exchange-list-create"
    ),

    path(
        "<int:pk>/status/",
        ExchangeStatusView.as_view(),
        name="exchange-status"
    ),

]