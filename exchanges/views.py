from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers

from .models import Exchange
from .serializers import ExchangeSerializer


class ExchangeListCreateView(
    generics.ListCreateAPIView
):

    serializer_class = ExchangeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Exchange.objects.filter(
            requester=user
        ) | Exchange.objects.filter(
            receiver=user
        )

    def perform_create(self, serializer):

        receiver = serializer.validated_data[
            "receiver"
        ]

        if receiver == self.request.user:
            raise serializers.ValidationError(
                "You cannot send a request to yourself."
            )

        serializer.save(
            requester=self.request.user
        )


class ExchangeStatusView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        try:
            exchange = Exchange.objects.get(
                pk=pk,
                receiver=request.user
            )

        except Exchange.DoesNotExist:
            return Response(
                {
                    "detail": "Exchange request not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get("status")

        if new_status not in [
            Exchange.ACCEPTED,
            Exchange.REJECTED
        ]:
            return Response(
                {
                    "detail": "Status must be accepted or rejected."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if exchange.status != Exchange.PENDING:
            return Response(
                {
                    "detail": "This request has already been processed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        exchange.status = new_status
        exchange.save()

        serializer = ExchangeSerializer(
            exchange
        )

        return Response(
            serializer.data
        )