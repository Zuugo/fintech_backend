from django.urls import path

from ledger import views

from .views import balances, submit_transaction

urlpatterns = [
    path("submit/", submit_transaction),
    path("balances/", balances),
    path("status/<str:tx_id>/", views.transaction_status),
]
