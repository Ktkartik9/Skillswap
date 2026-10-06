from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    reviewer_email = serializers.EmailField(
        source="reviewer.email",
        read_only=True
    )

    reviewed_user_email = serializers.EmailField(
        source="reviewed_user.email",
        read_only=True
    )

    class Meta:
        model = Review

        fields = [
            "id",
            "exchange",
            "reviewer",
            "reviewer_email",
            "reviewed_user",
            "reviewed_user_email",
            "rating",
            "comment",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "reviewer",
            "reviewer_email",
            "reviewed_user",
            "reviewed_user_email",
            "created_at",
        ]

    def validate_rating(self, value):

        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return value