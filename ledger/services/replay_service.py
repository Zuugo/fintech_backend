from ledger.models import ReplayEvent


class ReplayService:

    @staticmethod
    def log(event: str, details=None):

        ReplayEvent.objects.create(
            event=event,
            details=details or {},
        )
