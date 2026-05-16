from ledger.models import TransactionEvent, TransactionStatus


class StatusService:

    def update_transaction_status(tx_id: str, status: str, reason=None):
        tx_status, _ = TransactionStatus.objects.update_or_create(
            tx_id=tx_id,
            defaults={
                "status": status,
                "reason": reason,
            },
        )

        TransactionEvent.objects.create(
            tx_id=tx_id,
            event=status,
            details={
                "reason": reason,
            },
        )

        return tx_status

    @staticmethod
    def get_status(tx_id):
        try:
            tx = TransactionStatus.objects.get(tx_id=tx_id)

            return {
                "tx_id": tx.tx_id,
                "status": tx.status,
                "reason": tx.reason,
                "retries": tx.retries,
                "last_attempt_at": tx.last_attempt_at,
                "updated_at": tx.updated_at,
            }

        except TransactionStatus.DoesNotExist:
            return {
                "tx_id": tx_id,
                "status": "NOT FOUND",
                "reason": "Transaction not found",
            }
