from django.utils.timezone import now

from ledger.models import TransactionEvent, TransactionQueue, TransactionStatus


class TransactionLifecycleService:

    @staticmethod
    def transition(tx_id: str, status: str, reason=None):

        TransactionQueue.objects.filter(tx_id=tx_id).update(
            status=status,
            reason=reason,
            updated_at=now(),
        )

        TransactionStatus.objects.update_or_create(
            tx_id=tx_id,
            defaults={
                "status": status,
                "reason": reason,
                "last_attempt_at": now(),
            },
        )

        TransactionEvent.objects.create(
            tx_id=tx_id,
            event=status,
            details={
                "reason": reason,
            },
        )
