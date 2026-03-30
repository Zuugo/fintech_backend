from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import status

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
