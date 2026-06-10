from django.urls import path

from ledger import views

urlpatterns = [
    path("submit/", views.submit_transaction),
    path("balances/", views.balances),
    path("status/<str:tx_id>/", views.get_transaction_status),
    path("replay_events/", views.replay_events),
    path("timeline/", views.ledger_events),
    path("events/recover/", views.recover_events),
    path("projected-balances/", views.projected_balances),
    path("transactions/<str:tx_id>/timeline/", views.transaction_timeline),
    path("dead-letter/", views.dead_letter_queue),
    path("dead-letter/<str:tx_id>/replay/", views.replay_dead_letter),
    path("accounts/<str:account>/history/", views.AccountHistoryAPIView.as_view()),
    path("accounts/<str:account>/statement/", views.AccountStatementAPIView.as_view()),
    path(
        "accounts/<str:account>/statement/csv/", views.AccountStatementCSVView.as_view()
    ),
    path(
        "accounts/<str:account>/statement/pdf/", views.AccountStatementPDFView.as_view()
    ),
    path("snapshots/", views.SnapshotListView.as_view()),
    path("snapshots/<int:index>/restore/", views.SnapshotRestoreView.as_view()),
]
