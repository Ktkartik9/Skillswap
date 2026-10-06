from django.conf import settings
from django.db import models

from exchanges.models import Exchange


class Review(models.Model):

    exchange = models.ForeignKey(
        Exchange,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="given_reviews"
    )

    reviewed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_reviews"
    )

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "exchange",
                    "reviewer"
                ],
                name="one_review_per_exchange"
            )
        ]

    def __str__(self):
        return (
            f"{self.reviewer.email} → "
            f"{self.reviewed_user.email} "
            f"({self.rating}/5)"
        )