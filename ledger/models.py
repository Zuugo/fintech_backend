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
