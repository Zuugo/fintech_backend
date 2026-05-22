import json

from channels.generic.websocket import AsyncWebsocketConsumer


class LedgerConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        await self.channel_layer.group_add(
            "ledger_events",
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            "ledger_events",
            self.channel_name,
        )

    async def ledger_event(self, event):

        await self.send(
            text_data=json.dumps(
                {
                    "tx_id": event["tx_id"],
                    "event": event["event"],
                    "details": event["details"],
                }
            )
        )
