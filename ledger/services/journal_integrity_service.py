import json

from django.utils.crypto import hashlib

from ledger.engine import processor


class JournalIntegrityService:

    @staticmethod
    def verify():

        path = processor.journal.path

        if not path.exists():
            return {
                "healthy": False,
                "reason": "Journal file missing",
            }

        count = 0
        expected_previous_hash = "GENESIS"
        last_hash = None

        with open(path, "r", encoding="utf-8") as f:
            for line in f:

                data = json.loads(line.strip())

                stored_checksum = data["checksum"]

                checksum_record = dict(data)
                checksum_record.pop("checksum")

                calculated_checksum = hashlib.sha256(
                    json.dumps(checksum_record, sort_keys=True).encode()
                ).hexdigest()

                if stored_checksum != calculated_checksum:
                    return {
                        "healthy": False,
                        "reason": f"Checksum mismatch at {data['tx_id']}",
                    }

                stored_hash = data["hash"]

                record_for_hash = {
                    "tx_id": data["tx_id"],
                    "sender": data["sender"],
                    "receiver": data["receiver"],
                    "amount": data["amount"],
                    "nonce": data["nonce"],
                    "timestamp": data["timestamp"],
                    "previous_hash": data["previous_hash"],
                }

                calculated_hash = hashlib.sha256(
                    json.dumps(record_for_hash, sort_keys=True).encode()
                ).hexdigest()

                if stored_hash != calculated_hash:
                    return {
                        "healthy": False,
                        "reason": f"Hash mismatch at {data['tx_id']}",
                    }

                if data["previous_hash"] != expected_previous_hash:
                    return {
                        "healthy": False,
                        "reason": f"Broken hash chain at {data['tx_id']}",
                    }

                expected_previous_hash = data["hash"]
                last_hash = data["hash"]

                count += 1

        return {
            "healthy": True,
            "records": count,
            "last_hash": last_hash,
        }
