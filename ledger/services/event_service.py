from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from ledger.models import LedgerEvent
from ledger.services.projection_service import ProjectionService


class EventService:

    @staticmethod
    def emit(tx_id, event, details=None):

        print(f"[EVENT EMIT] {event} tx={tx_id}")

        db_event = LedgerEvent.objects.create(
            tx_id=tx_id,
            event=event,
            details=details or {},
        )

        payload = {
            "sequence": db_event.sequence,
            "tx_id": db_event.tx_id,
            "event": db_event.event,
            "details": db_event.details,
        }

        ProjectionService.apply(db_event)

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "ledger_events",
            {
                "type": "ledger_event",
                **payload,
            },
        )
