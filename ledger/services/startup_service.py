from ledger.services.event_service import EventService
from ledger.services.journal_integrity_service import JournalIntegrityService
from ledger.services.replay_service import ReplayService
from ledger.services.snapshot_integrity_service import SnapshotIntegrityService
from ledger.services.startup_context import StartupContext


class StartupService:

    def __init__(self, processor):
        self.processor = processor

    def start(self):

        context = StartupContext()

        self._restore_snapshot(context)

        self._verify_snapshot(context)

        self._replay_journal(context)

        self._verify_journal(context)

        self._complete_startup(context)

    def _restore_snapshot(self, context):

        snapshot = self.processor.replay_engine.restore_from_snapshot()

        if snapshot:
            context.snapshot_loaded = True
            context.snapshot_id = snapshot["snapshot_id"]
            context.journal_position = snapshot["journal_position"]
            context.last_hash = snapshot["last_hash"]

        ReplayService.log(
            "SNAPSHOT_RESTORED",
            {
                "journal_position": context.journal_position,
            },
        )

        EventService.emit(
            None,
            "SNAPSHOT_RESTORED",
            {
                "journal_position": context.journal_position,
            },
        )

    def _replay_journal(self, context):

        transactions = self.processor.journal.load_from(context.journal_position)

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

        context.replayed_transactions = len(transactions)

        return transactions

    def _complete_startup(self, context):

        context.balances = dict(self.processor.ledger.balances)
        context.nonces = dict(self.processor.ledger.nonces)

        ReplayService.log(
            "REPLAY_COMPLETED",
            {
                "balances": context.balances,
                "nonces": context.nonces,
            },
        )

        EventService.emit(
            None,
            "REPLAY_COMPLETED",
            {
                "balances": context.balances,
                "nonces": context.nonces,
            },
        )

    def _verify_snapshot(self, context):

        if not context.snapshot_loaded:
            return

        result = SnapshotIntegrityService.verify(context.snapshot_id)

        if not result["healthy"]:
            raise RuntimeError(result["reason"])

        context.snapshot_verified = True

        ReplayService.log(
            "SNAPSHOT_VERIFIED",
            result,
        )

        EventService.emit(
            None,
            "SNAPSHOT_VERIFIED",
            result,
        )

    def _verify_journal(self, context):

        result = JournalIntegrityService.verify()

        if not result["healthy"]:
            raise RuntimeError(result["reason"])

        context.journal_verified = True

        ReplayService.log("JOURNAL_VERIFIED", result)

        EventService.emit(None, "JOURNAL_VERIFIED", result)
