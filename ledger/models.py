from django.db import models


class TransactionStatus(models.Model):
    tx_id = models.CharField(max_length=100, unique=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("PROCESSING", "Processing"),
            ("RETRY", "Retry"),
            ("SUCCESS", "Success"),
            ("FAILED", "Failed"),
            ("BUFFERED", "Buffered"),
        ],
    )
    reason = models.TextField(null=True, blank=True)
    retries = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    last_attempt_at = models.DateTimeField(null=True, blank=True)


class TransactionQueue(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("RETRY", "Retry"),
        ("FAILED", "Failed"),
        ("SUCCESS", "Success"),
        ("BUFFERED", "Buffered"),
    ]

    tx_id = models.CharField(max_length=100, unique=True)

    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    amount = models.FloatField()
    nonce = models.IntegerField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    retries = models.IntegerField(default=0)
    next_attempt = models.DateTimeField(null=True, blank=True)

    reason = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processing_started_at = models.DateTimeField(null=True, blank=True)


class TransactionEvent(models.Model):
    tx_id = models.CharField(max_length=255)

    event = models.CharField(max_length=55)

    details = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tx_id} -> {self.event}"


class ReplayEvent(models.Model):

    event = models.CharField(max_length=55)

    details = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event}"


class LedgerEvent(models.Model):
    sequence = models.BigAutoField(unique=True, primary_key=True)

    tx_id = models.CharField(max_length=255, null=True)

    event = models.CharField(max_length=55)
    details = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tx_id} -> {self.event}"


class AccountProjection(models.Model):

    account = models.CharField(max_length=255, unique=True)

    balance = models.FloatField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account}: {self.balance}"
