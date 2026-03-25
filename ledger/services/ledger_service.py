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

        success = processor.process(tx)

        return {"success": success}

    def get_balances(self):
        return processor.ledger.get_balances()
