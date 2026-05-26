from threading import active_count

from ledger.models import AccountProjection


class ProjectionService:

    @staticmethod
    def apply(e):

        if e.event not in ("TX_SUCCESS", "SUCCESS"):
            return

        details = e.details

        sender = details["sender"]
        receiver = details["receiver"]
        amount = details["amount"]

        if sender != "SYSTEM":

            sender_projection, _ = AccountProjection.objects.get_or_create(
                account=sender,
            )

            sender_projection.balance -= amount
            sender_projection.save()

        receiver_projection, _ = AccountProjection.objects.get_or_create(
            account=receiver,
        )

        receiver_projection.balance += amount
        receiver_projection.save()
