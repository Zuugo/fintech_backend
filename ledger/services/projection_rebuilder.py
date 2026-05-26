from ledger.models import AccountProjection, LedgerEvent
from ledger.services.projection_service import ProjectionService


class ProjectionRebuilder:

    @staticmethod
    def rebuild():

        print(f"[PROJECTION REBUILD] starting...")

        AccountProjection.objects.all().delete()

        events = LedgerEvent.objects.filter(
            event="TX_SUCCESS" or "SUCCESS",
        ).order_by("sequence")

        for e in events:
            ProjectionService.apply(e)

        print(f"[PROJECTION REBUILD] completed")
