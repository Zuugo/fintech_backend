from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from ledger.models import LedgerEvent


class EventService:

    @staticmethod
    def emit(tx_id, event, details=None):

        print(f"[EVENT EMIT] {event} tx={tx_id}")

        payload = {
            "tx_id": tx_id,
            "event": event,
            "details": details or {},
        }

        LedgerEvent.objects.create(**payload)

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "ledger_events",
            {
                "type": "ledger_event",
                **payload,
            },
        )
