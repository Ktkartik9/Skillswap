from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True
    )

    def validate(self, data):

        email = data.get("email")
        password = data.get("password")

        user = authenticate(
            username=email,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "bio",
            "location",
            "profile_image",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "email",
            "created_at",
        ]