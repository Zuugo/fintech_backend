from rest_framework import serializers

from ledger.models import DeadLetterQueue, LedgerEvent


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


class DeadLetterQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeadLetterQueue

        fields = "__all__"
