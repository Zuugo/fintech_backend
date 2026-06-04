from ledger.models import LedgerEvent


class AccountHistoryService:

    @staticmethod
    def get_history(account):

        transactions = []

        success_events = LedgerEvent.objects.filter(event="TX_SUCCESS").order_by(
            "sequence"
        )

        for event in success_events:

            sender = event.details.get("sender")
            receiver = event.details.get("receiver")

            if account not in [sender, receiver]:
                continue

            transactions.append(
                {
                    "tx_id": event.tx_id,
                    "sender": sender,
                    "receiver": receiver,
                    "amount": event.details.get("amount"),
                }
            )

        return transactions
