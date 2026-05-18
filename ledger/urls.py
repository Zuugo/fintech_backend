from django.urls import path

from ledger import views

urlpatterns = [
    path("submit/", views.submit_transaction),
    path("balances/", views.balances),
    path("status/<str:tx_id>/", views.get_transaction_status),
    path("replayevents/", views.replay_events),
]
