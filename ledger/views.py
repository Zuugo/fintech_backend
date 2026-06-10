from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView, status

from ledger.engine import status_store
from ledger.serializers import DeadLetterQueueSerializer, LedgerEventSerializer
from ledger.services.account_history_service import AccountHistoryService
from ledger.services.account_statement_service import AccountStatementService
from ledger.services.event_service import EventService
from ledger.services.pdf_statement_service import PDFStatementService
from ledger.services.snapshot_service import SnapshotService
from ledger.services.statement_export_service import StatementExportService
from ledger.services.status_service import StatusService
from ledger.services.timeline_service import TimelineService

from .models import (
    AccountProjection,
    DeadLetterQueue,
    LedgerEvent,
    ReplayEvent,
    TransactionQueue,
    TransactionStatus,
)
from .services.ledger_service import LedgerService

service = LedgerService()


@api_view(["POST"])
def submit_transaction(request):
    result = service.submit_transaction(request.data)

    if result["status"] == "error":
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    return Response(result, status=status.HTTP_200_OK)


@api_view(["POST"])
def replay_dead_letter(request, tx_id):

    dead_letter_tx = DeadLetterQueue.objects.get(tx_id=tx_id)

    job = TransactionQueue.objects.get(tx_id=tx_id)

    job.status = "PENDING"
    job.retries = 0
    job.reason = None
    job.processing_started_at = None
    job.save()

    dead_letter_tx.delete()

    EventService.emit(tx_id, "DLQ_REPLAYED", {})

    return Response({"status": "requeued", "tx_id": tx_id})


@api_view(["GET"])
def balances(request):
    return Response(service.get_balances(), status=status.HTTP_200_OK)


"""
@api_view(["GET"])
def transaction_status(request, tx_id):
    try:
        tx = TransactionStatus.objects.get(tx_id=tx_id)

        return JsonResponse({"status": tx.status, "reason": tx.reason})

    except TransactionStatus.DoesNotExist:
        return JsonResponse({"status": "UNKNOWN", "reason": None})

"""


@api_view(["GET"])
def get_transaction_status(request, tx_id):
    result = StatusService.get_status(tx_id)
    return Response(result)


@api_view(["GET"])
def replay_events(request):

    events = ReplayEvent.objects.order_by("-created_at")[:50]

    data = [
        {
            "event": e.event,
            "details": e.details,
            "created_at": e.created_at,
        }
        for e in events
    ]

    return Response(data)


@api_view(["GET"])
def ledger_events(request):

    events = LedgerEvent.objects.all().order_by("created_at")

    data = [
        {
            "tx_id": e.tx_id,
            "event": e.event,
            "details": e.details,
            "created_at": e.created_at,
        }
        for e in events
    ]

    return Response(data)


@api_view(["GET"])
def recover_events(request):

    after = request.GET.get("after", 0)

    events = LedgerEvent.objects.filter(sequence__gt=after).order_by("sequence")

    data = [
        {
            "sequence": e.sequence,
            "tx_id": e.tx_id,
            "event": e.event,
            "details": e.details,
            "created_at": e.created_at,
        }
        for e in events
    ]

    return Response(data)


@api_view(["GET"])
def projected_balances(request):

    projections = AccountProjection.objects.all()

    data = [{p.account: p.balance} for p in projections]

    return Response(data)


@api_view(["GET"])
def transaction_timeline(request, tx_id):

    events = TimelineService.get_transaction_timeline(tx_id)

    serializer = LedgerEventSerializer(events, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def dead_letter_queue(request):

    records = DeadLetterQueue.objects.order_by("-created_at")

    serializer = DeadLetterQueueSerializer(records, many=True)

    return Response(serializer.data)


class AccountHistoryAPIView(APIView):

    def get(self, request, account):

        history = AccountHistoryService.get_history(account)

        return Response(history)


class AccountStatementAPIView(APIView):

    def get(self, request, account):

        statement = AccountStatementService.generate_statement(account)

        return Response(statement)


class AccountStatementCSVView(APIView):

    def get(self, request, account):

        csv_data = StatementExportService.export_csv(account)

        response = HttpResponse(
            csv_data,
            content_type="text/csv",
        )

        response["Content-Disposition"] = (
            f"attachment; " f'filename="{account}_statement.csv"'
        )

        return response


class AccountStatementPDFView(APIView):

    def get(self, request, account):

        pdf = PDFStatementService.generate_pdf(account)

        response = HttpResponse(pdf, content_type="application/pdf")

        response["Content-Disposition"] = (
            f"attachment; " f"filename='{account}statement.pdf'"
        )

        return response


class SnapshotListView(APIView):

    def get(self, request):

        return Response(SnapshotService.list_snapshots())


class SnapshotRestoreView(APIView):

    def post(self, request, index):

        snapshot = SnapshotService.restore_snapshot(index)

        return Response(
            {
                "status": "restored",
                "snapshot": index,
            }
        )
