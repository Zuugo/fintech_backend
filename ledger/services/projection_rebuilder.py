from ledger_engine.storage.transaction_journal import TransactionJournal

from ledger.models import AccountProjection


class ProjectionRebuilder:

    @staticmethod
    def rebuild():

        print("[PROJECTION REBUILD] starting")

        AccountProjection.objects.all().delete()

        journal = TransactionJournal("data/journal.log")

        transactions = journal.load_from(0)

        projections = {}

        print(f"TRANSACTIONS:")

        for tx in transactions:

            print(tx.tx_id, tx.sender, tx.receiver, tx.amount)

            if tx.sender != "SYSTEM":

                projections[tx.sender] = projections.get(tx.sender, 0) - tx.amount

            projections[tx.receiver] = projections.get(tx.receiver, 0) + tx.amount

        print(f"FINAL PROJECTIONS", projections)
        for account, balance in projections.items():

            AccountProjection.objects.create(
                account=account,
                balance=balance,
            )

        print("[PROJECTION REBUILD] completed")
