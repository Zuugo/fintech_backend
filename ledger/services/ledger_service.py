import time

from ledger_engine.models.transaction import Transaction

from ledger.engine import processor, tx_queue


class LedgerService:

    def submit_transaction(self, data):
        tx = Transaction(
            tx_id=data["tx_id"],
            sender=data["sender"],
            receiver=data.get("receiver"),
            amount=data["amount"],
            nonce=data["nonce"],
            timestamp=time.time(),
        )

        tx_queue.enqueue(tx)

        return {"status": "queued", "tx_id": tx.tx_id}

    def get_balances(self):
        return processor.ledger.get_balances()
