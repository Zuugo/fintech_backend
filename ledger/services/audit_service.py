from pathlib import Path

from ledger.engine import processor
from ledger.models import (
    AccountProjection,
    DeadLetterQueue,
    LedgerEvent,
    TransactionQueue,
)
from ledger.services.snapshot_service import SnapshotService


class AuditService:

    @staticmethod
    def summary():

        return {
            "successful_transactions": LedgerEvent.objects.filter(
                event="TX_SUCCESS"
            ).count(),
            "failed_transactions": LedgerEvent.objects.filter(
                event="TX_FAILED"
            ).count(),
            "dlq_transactions": DeadLetterQueue.objects.count(),
            "replayed_transactions": LedgerEvent.objects.filter(event="TX_REPLAY")
            .values("tx_id")
            .distinct()
            .count(),
            "snapshots": len(SnapshotService.list_snapshots()),
            "queued_transactions": TransactionQueue.objects.filter(
                status="PENDING"
            ).count(),
        }

    @staticmethod
    def events():

        return list(
            LedgerEvent.objects.order_by("sequence").values(
                "sequence", "event", "tx_id", "created_at"
            )
        )

    @staticmethod
    def integrity():

        projection = {}

        for row in AccountProjection.objects.all():

            projection[row.account] = row.balance

        ledger_balances = processor.ledger.balances

        matches = projection == ledger_balances

        return {
            "ledger_matches_projection": matches,
            "journal_exists": Path("data/journal.log").exists(),
            "projection_accounts": len(projection),
            "ledger_accounts": len(ledger_balances),
            "status": "HEALTHY" if matches else "CORRUPTED",
        }
