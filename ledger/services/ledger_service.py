import time

from ledger_engine.models.transaction import Transaction

from ledger.engine import processor
from ledger.models import TransactionStatus
from ledger.shared.state import status_store, tx_queue


class LedgerService:

    def submit_transaction(self, data):
        tx_id = data["tx_id"]

        existing = status_store.get_status(tx_id)

        if existing["status"] != "UNKNOWN":
            return {"status": "error", "reason": "Transaction already submitted"}
        tx = Transaction(
            tx_id=tx_id,
            sender=data["sender"],
            receiver=data.get("receiver"),
            amount=data["amount"],
            nonce=data["nonce"],
            timestamp=time.time(),
        )

        tx_queue.enqueue({"tx": tx, "retries": 0, "next_attempt": time.time()})

        TransactionStatus.objects.update_or_create(
            tx_id=tx.tx_id, defaults={"status": "PENDING", "reason": None}
        )

        return {"status": "queued", "tx_id": tx.tx_id}

    def get_balances(self):
        return processor.ledger.get_balances()
