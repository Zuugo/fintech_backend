from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services.ledger_service import LedgerService

service = LedgerService()


@api_view(["POST"])
def submit_transaction(request):
    return Response(service.submit_transaction(request.data))


@api_view(["GET"])
def balances(request):
    return Response(service.get_balances())
