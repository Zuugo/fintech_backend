from django.utils.timezone import now

from .models import TransactionQueue


def recover_pending_transactions():
    recovered = TransactionQueue.objects.filter(status="PROCESSING")

    count = 0

    for job in recovered:
        job.status = "RETRY"
        job.next_attempt = now().timestamp()
        job.processing_started_at = None
        job.save()

        count += 1

    print(f"[RECOVERY] Recovered {count} stuck jobs")
