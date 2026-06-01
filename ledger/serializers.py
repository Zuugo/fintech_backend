from rest_framework import serializers

from ledger.models import LedgerEvent


class LedgerEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = LedgerEvent

        fields = [
            "sequence",
            "tx_id",
            "event",
            "details",
            "created_at",
        ]
