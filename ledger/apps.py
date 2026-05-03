import threading

from django.apps import AppConfig
from django.utils.autoreload import sys


class LedgerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ledger"

    def ready(self):
        import os

        if os.environ.get("RUN MAIN") != "true":
            return

        if "migrate" in sys.argv or "makemigrations" in sys.argv:
            return

        from ledger.engine import recover_pending_transactions, worker

        recover_pending_transactions()

        t = threading.Thread(target=worker.run, daemon=True)
        t.start()
