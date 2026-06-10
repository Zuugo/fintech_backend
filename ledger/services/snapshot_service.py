import json
from pathlib import Path

from ledger.engine import processor
from ledger.services.event_service import EventService


class SnapshotService:

    SNAPSHOT_DIR = Path("data")

    @classmethod
    def list_snapshots(cls):

        snapshots = []

        for file in cls.SNAPSHOT_DIR.glob("snapshot_*.json"):

            snapshots.append(
                {
                    "index": int(file.stem.split("_")[1]),
                    "file": file.name,
                }
            )

        return sorted(snapshots, key=lambda x: x["index"])

    @classmethod
    def restore_snapshot(cls, index):

        file_path = cls.SNAPSHOT_DIR / f"snapshot_{index}.json"

        if not file_path.exists():
            raise FileNotFoundError(f"snapshot_{index}.json not found")

        with open(file_path) as f:
            snapshot = json.load(f)

            processor.ledger.balances = snapshot["balances"]
            processor.ledger.nonces = snapshot["nonces"]
            processor.ledger.processed_ids = set(snapshot["processed_ids"])
            processor.ledger.future_transactions = snapshot.get(
                "future_transactions", {}
            )

            EventService.emit(
                None,
                "SNAPSHOT_RESTORED",
                {
                    "snapshot_index": index,
                },
            )

        return snapshot
