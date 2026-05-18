from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import status

from ledger.engine import status_store
from ledger.services.status_service import StatusService

from .models import ReplayEvent, TransactionStatus
from .services.ledger_service import LedgerService

service = LedgerService()


@api_view(["POST"])
def submit_transaction(request):
    result = service.submit_transaction(request.data)

    if result["status"] == "error":
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    return Response(result, status=status.HTTP_200_OK)


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
