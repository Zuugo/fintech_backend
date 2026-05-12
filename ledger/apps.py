import sys
import threading

from django.apps import AppConfig
from django.db import connections
from django.db.utils import OperationalError, ProgrammingError


class LedgerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ledger"

    def ready(self):
        import os

        if os.environ.get("RUN_MAIN") != "true":
            return

        if any(cmd in sys.argv for cmd in ["migrate", "makemigrations"]):
            return

        try:
            from ledger.models import TransactionQueue

            TransactionQueue.objects.exists()
        except (OperationalError, ProgrammingError) as e:
            print(f"[WORKER] DB/schema not ready: {e}")
            return

        def start_worker():

            from ledger.engine import worker
            from ledger.recovery import recover_pending_transactions

            recover_pending_transactions()

            worker.start()

        threading.Timer(1.0, start_worker).start()
