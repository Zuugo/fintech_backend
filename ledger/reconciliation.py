from ledger.models import TransactionQueue, TransactionStatus


def reconcile_ledger_state(processed_ids):

    restored = 0

    for tx_id in processed_ids:

        TransactionQueue.objects.filter(tx_id=tx_id).update(status="SUCCESS")

        TransactionStatus.objects.update_or_create(
            tx_id=tx_id,
            defaults={
                "status": "SUCCESS",
                "reason": None,
            },
        )

        restored += 1

    print(f"[RECONCILE] Restored {restored} transaction statuses")
