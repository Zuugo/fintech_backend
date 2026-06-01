from ledger.models import LedgerEvent


class TimelineService:

    @staticmethod
    def get_transaction_timeline(tx_id):

        return LedgerEvent.objects.filter(tx_id=tx_id).order_by("sequence")
