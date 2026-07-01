import hashlib

from ledger.services.snapshot_service import SnapshotService


class SnapshotIntegrityService:

    @staticmethod
    def verify(index):

        snapshot_file = SnapshotService.SNAPSHOT_DIR / f"snapshot_{index}.json"
        checksum_file = SnapshotService.SNAPSHOT_DIR / f"snapshot_{index}.sha256"

        if not snapshot_file.exists():
            return {"healthy": False, "reason": "Snapshot missing"}

        if not checksum_file.exists():
            return {"healthy": False, "reason": "Checksum missing"}

        with open(snapshot_file) as f:
            snapshot_content = f.read()

        with open(checksum_file) as f:
            stored_checksum = f.read().strip()

        calculated_checksum = hashlib.sha256(snapshot_content.encode()).hexdigest()

        if stored_checksum != calculated_checksum:
            return {"healthy": False, "reason": "Snapshot checksum mismatch"}

        return {"healthy": True, "snapshot": index}
