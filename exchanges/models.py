from django.conf import settings
from django.db import models


class Exchange(models.Model):

    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected"),
    ]

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_exchanges"
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_exchanges"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    message = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["requester", "receiver"],
                name="unique_exchange_request"
            )
        ]

    def __str__(self):
        return (
            f"{self.requester.email} → "
            f"{self.receiver.email} "
            f"({self.status})"
        )