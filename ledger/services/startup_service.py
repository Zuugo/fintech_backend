from ledger.services.event_service import EventService
from ledger.services.replay_service import ReplayService


class StartupService:

    def __init__(self, processor):
        self.processor = processor

    def start(self):

        journal_position = self._restore_snapshot()

        self._replay_journal(journal_position)

        self._complete_startup()

    def _restore_snapshot(self):

        journal_position = self.processor.replay_engine.restore_from_snapshot()

        ReplayService.log(
            "SNAPSHOT_RESTORED",
            {
                "journal_position": journal_position,
            },
        )

        EventService.emit(
            None,
            "SNAPSHOT_RESTORED",
            {
                "journal_position": journal_position,
            },
        )

        return journal_position

    def _replay_journal(self, journal_position):

        transactions = self.processor.journal.load_from(journal_position)

        ReplayService.log("JOURNAL_REPLAY_STARTED", {"count": len(transactions)})

        EventService.emit(None, "JOURNAL_REPLAY_STARTED", {"count": len(transactions)})

        for tx in transactions:

            print(f"[REPLAY TX] {tx.tx_id}")

            ReplayService.log(
                "TX_REPLAY",
                {
                    "tx_id": tx.tx_id,
                },
            )

            EventService.emit(
                tx.tx_id,
                "TX_REPLAY",
                {
                    "tx_id": tx.tx_id,
                },
            )

            if tx.tx_id in self.processor.ledger.processed_ids:
                continue

            self.processor.ledger.apply_transaction(tx)

        return transactions

    def _complete_startup(self):

        ReplayService.log(
            "REPLAY_COMPLETED",
            {
                "balances": self.processor.ledger.balances,
                "nonces": self.processor.ledger.nonces,
            },
        )

        EventService.emit(
            None,
            "REPLAY_COMPLETED",
            {
                "balances": self.processor.ledger.balances,
                "nonces": self.processor.ledger.nonces,
            },
        )
