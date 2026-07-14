import json
from pathlib import Path


class EngineMetadataService:

    METADATA_FILE = Path("data/engine_state.json")

    @classmethod
    def load(cls):

        if not cls.METADATA_FILE.exists():
            return {
                "tx_count": 0,
                "tx_since_snapshot": 0,
                "last_snapshot_id": None,
                "last_snapshot_position": 0,
            }

        with open(cls.METADATA_FILE, "r") as f:
            return json.load(f)

    @classmethod
    def save(
        cls, tx_count, tx_since_snapshot, last_snapshot_id, last_snapshot_position
    ):

        cls.METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        metadata = {
            "tx_count": tx_count,
            "tx_since_snapshot": tx_since_snapshot,
            "last_snapshot_id": last_snapshot_id,
            "last_snapshot_position": last_snapshot_position,
        }

        with open(cls.METADATA_FILE, "w") as f:
            json.dump(metadata, f, indent=2)
