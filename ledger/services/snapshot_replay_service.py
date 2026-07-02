from ledger.engine import journal, processor
from ledger.services.event_service import EventService


class SnapshotReplayService:

    @staticmethod
    def replay_after_snapshot(snapshot):

        journal_position = snapshot["journal_position"]

        transactions = journal.load_from(journal_position)

        for transaction in transactions:

            if transaction.tx_id in processor.ledger.processed_ids:
                continue

            print(f"[SNAPSHOT REPLAY] {transaction.tx_id}")

            processor.ledger.apply_transaction(transaction)

            EventService.emit(
                transaction.tx_id,
                "TX_REPLAY",
                {
                    "tx_id": transaction.tx_id,
                },
            )

        EventService.emit(
            None,
            "REPLAY COMPLETED",
            {
                "count": len(transactions),
            },
        )
