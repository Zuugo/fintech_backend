from ledger_engine.models.transaction import Transaction


def recover_pending_transactions():
    from ledger.engine import tx_queue

    from .models import TransactionStatus

    pending_txs = TransactionStatus.objects.filter(status="PENDING")

    for tx_record in pending_txs:
        tx = Transaction(
            tx_id=tx_record.tx_id,
            sender=tx_record.sender,
            receiver=tx_record.receiver,
            amount=tx_record.amount,
            nonce=tx_record.nonce,
            timestamp=tx_record.timestamp,
        )

        item = {
            "tx": tx,
            "retries": 0,
            "next_attempt": 0,
        }

        tx_queue.enqueue(item)

    print(f"[RECOVERY] Requeued {pending_txs.count()} transactions")
