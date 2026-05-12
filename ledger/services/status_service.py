from ledger.models import TransactionStatus


class StatusService:

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
