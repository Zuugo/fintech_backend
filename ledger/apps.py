import os
import sys
import threading

worker_started = False
lock = threading.Lock()

from django.apps import AppConfig


class LedgerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ledger"

    def ready(self):

        global worker_started

        with lock:
            if worker_started:
                return

            worker_started = True

        if any(cmd in sys.argv for cmd in ["migrate", "makemigrations"]):
            return

        def start_worker():

            try:

                from ledger.engine import processor, worker
                from ledger.reconciliation import reconcile_ledger_state
                from ledger.recovery import recover_pending_transactions

                processor.start()

                reconcile_ledger_state(processor.ledger.processed_ids)

                recover_pending_transactions()

                worker.start()

            except Exception as e:
                print(f"[STARTUP ERROR] {e}")

        threading.Timer(1.0, start_worker).start()
