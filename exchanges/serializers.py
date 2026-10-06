from rest_framework import serializers

from .models import Exchange


class ExchangeSerializer(serializers.ModelSerializer):

    requester_email = serializers.EmailField(
        source="requester.email",
        read_only=True
    )

    receiver_email = serializers.EmailField(
        source="receiver.email",
        read_only=True
    )

    class Meta:
        model = Exchange

        fields = [
            "id",
            "requester",
            "requester_email",
            "receiver",
            "receiver_email",
            "status",
            "message",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "requester",
            "requester_email",
            "receiver_email",
            "status",
            "created_at",
            "updated_at",
        ]