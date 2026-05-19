from ledger.models import LedgerEvent


class EventService:

    @staticmethod
    def emit(tx_id, event, details=None):

        LedgerEvent.objects.create(
            tx_id=tx_id,
            event=event,
            details=details or {},
        )
