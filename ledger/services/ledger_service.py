import time

from ledger_engine.models.transaction import Transaction

from ledger.engine import processor


class LedgerService:

    def submit_transaction(self, data):
        tx = Transaction(
            tx_id=data["tx_id"],
            sender=data["sender"],
            receiver=data["receiver"],
            amount=data["amount"],
            nonce=data["nonce"],
            timestamp=time.time(),
        )

        if not processor.validate.validate(tx):
            return {"status": "error", "reason": "Invalid transaction"}

        success, reason = processor.process(tx)

        if not success:
            return {"status": "error", "reason": reason}

        return {"status": "success", "tx_id": tx.tx_id}

    def get_balances(self):
        return processor.ledger.get_balances()
