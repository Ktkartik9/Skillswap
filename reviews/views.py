from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from .models import Review
from .serializers import ReviewSerializer
from exchanges.models import Exchange


class ReviewListCreateView(
    generics.ListCreateAPIView
):

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(
            reviewed_user=self.request.user
        )

    def perform_create(self, serializer):

        exchange_id = self.request.data.get(
            "exchange"
        )

        try:
            exchange = Exchange.objects.get(
                id=exchange_id
            )
        except Exchange.DoesNotExist:
            raise serializers.ValidationError(
                "Exchange does not exist."
            )

        # User must be part of the exchange
        if (
            exchange.requester != self.request.user
            and
            exchange.receiver != self.request.user
        ):
            raise serializers.ValidationError(
                "You are not part of this exchange."
            )

        # Exchange must be accepted
        if exchange.status != Exchange.ACCEPTED:
            raise serializers.ValidationError(
                "You can review only an accepted exchange."
            )

        # Decide who receives the review
        if exchange.requester == self.request.user:
            reviewed_user = exchange.receiver
        else:
            reviewed_user = exchange.requester

        serializer.save(
            reviewer=self.request.user,
            reviewed_user=reviewed_user,
        )