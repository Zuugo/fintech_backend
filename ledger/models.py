from django.db import models


class TransactionStatus(models.Model):
    tx_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20)
    reason = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tx_id} - {self.status}"
