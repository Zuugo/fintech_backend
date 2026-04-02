from ledger_engine.core.ledger import Ledger
from ledger_engine.execution.processor import TransactionProcessor
from ledger_engine.queue.transaction_queue import TransactionQueue
from ledger_engine.queue.worker import TransactionWorker
from ledger_engine.replay.replay_engine import ReplayEngine
from ledger_engine.storage.snapshot_store import SnapshotStore
from ledger_engine.storage.transaction_journal import TransactionJournal
from ledger_engine.validation.validator import TransactionValidator

ledger = Ledger()

journal = TransactionJournal("data/journal.log")
snapshot_store = SnapshotStore("data")

replay = ReplayEngine(ledger, snapshot_store)
validator = TransactionValidator()

processor = TransactionProcessor(
    ledger,
    journal,
    snapshot_store,
    replay,
    validator,
    snapshot_interval=5,
)

# restore state on server start

processor.start()

tx_queue = TransactionQueue()

worker = TransactionWorker(tx_queue, processor)
worker.start()
