import os
import sys
import threading

from django.apps import AppConfig


class LedgerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ledger"

    def ready(self):

        if os.environ.get("RUN_MAIN") != "true":
            return

        if any(cmd in sys.argv for cmd in ["migrate", "makemigrations"]):
            return

        def start_worker():

            try:

                from ledger.engine import processor, worker
                from ledger.recovery import recover_pending_transactions

                processor.start()

                recover_pending_transactions()

                worker.start()

            except Exception as e:
                print(f"[STARTUP ERROR] {e}")

        threading.Timer(1.0, start_worker).start()
