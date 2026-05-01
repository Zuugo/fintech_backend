import time

from django.db import IntegrityError
from ledger_engine.models.transaction import Transaction

from ledger.engine import processor
from ledger.models import TransactionQueue, TransactionStatus
from ledger.shared.state import status_store, tx_queue


class LedgerService:

    def submit_transaction(self, data):
        tx_id = data["tx_id"]

        try:
            TransactionQueue.objects.create(
                tx_id=tx_id,
                sender=data["sender"],
                receiver=data["receiver"],
                amount=data["amount"],
                nonce=data["nonce"],
                status="PENDING",
                next_attempt=time.time(),
            )

        except IntegrityError:
            return {"status": "DUPLICATE", "tx_id": tx_id}

        TransactionStatus.objects.update_or_create(
            tx_id=tx_id,
            defaults={
                "status": "PENDING",
                "reason": None,
            },
        )

        return {"status": "queued", "tx_id": tx_id}

    def get_balances(self):
        return processor.ledger.get_balances()
