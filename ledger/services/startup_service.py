from ledger.services.audit_service import AuditService
from ledger.services.engine_metadata_service import EngineMetadataService
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

        self._restore(context)

        self._verify(context)

        self._runtime(context)

    def _restore(self, context):

        self._restore_snapshot(context)

        self._restore_engine_metadata(context)

        self._replay_journal(context)

    def _verify(self, context):

        self._verify_snapshot(context)

        self._verify_journal(context)

        self._verify_ledger(context)

    def _runtime(self, context):

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

    def _replay_journal(self, context):

        transactions = self.processor.journal.load_from(context.journal_position)

        ReplayService.log("JOURNAL_REPLAY_STARTED", {"count": len(transactions)})

        for tx in transactions:

            print(f"[REPLAY TX] {tx.tx_id}")

            ReplayService.log(
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

    def _verify_ledger(self, context):

        result = AuditService.integrity()

        if not result["ledger_matches_projection"]:
            raise RuntimeError(f"Ledger state does not match projection")

        context.ledger_verified = True

        ReplayService.log("LEDGER_VERIFIED", result)

        EventService.emit(None, "LEDGER_VERIFIED", result)

    def _restore_engine_metadata(self, context):

        state = EngineMetadataService.load()

        self.processor.tx_count = state["tx_count"]
        self.processor.tx_since_snapshot = state["tx_since_snapshot"]

        context.last_snapshot_id = state["last_snapshot_id"]
        context.last_snapshot_position = state["last_snapshot_position"]

        print(
            "[ENGINE STATE]", self.processor.tx_count, self.processor.tx_since_snapshot
        )
