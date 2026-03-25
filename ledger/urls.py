from django.urls import path

from .views import balances, submit_transaction

urlpatterns = [
    path("submit/", submit_transaction),
    path("balances/", balances),
]
