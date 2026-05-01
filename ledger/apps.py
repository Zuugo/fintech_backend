import threading

from django.apps import AppConfig


class LedgerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ledger"

    def ready(self):
        import os

        if os.environ.get("RUN MAIN") != "true":
            return

        from ledger.engine import recover_pending_transactions, worker

        recover_pending_transactions()

        t = threading.Thread(target=worker.run, daemon=True)
        t.start()
