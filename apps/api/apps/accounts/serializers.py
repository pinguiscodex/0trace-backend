from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "handle",
            "email",
            "display_name",
            "preferred_language",
            "timezone",
            "onboarding_completed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "onboarding_completed_at"]


class SignupSerializer(serializers.Serializer):
    handle = serializers.SlugField(max_length=32)
    email = serializers.EmailField()
    display_name = serializers.CharField(max_length=80, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, min_length=10, trim_whitespace=False)
    terms_accepted = serializers.BooleanField()

    def validate_terms_accepted(self, value: bool) -> bool:
        if not value:
            raise serializers.ValidationError("Terms must be accepted.")
        return value

    def validate_handle(self, value: str) -> str:
        value = value.lower()
        if User.objects.filter(handle=value).exists():
            raise serializers.ValidationError("Handle is already taken.")
        return value

    def validate_email(self, value: str) -> str:
        value = value.lower()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        identifier = attrs["identifier"].lower()
        password = attrs["password"]
        user = authenticate(self.context["request"], username=identifier, password=password)
        if user is None:
            raise serializers.ValidationError({"identifier": "Invalid credentials."})
        if not user.is_active:
            raise serializers.ValidationError({"identifier": "Account is inactive."})
        attrs["user"] = user
        return attrs


class SessionSerializer(serializers.Serializer):
    authenticated = serializers.BooleanField()
    user = UserSerializer(allow_null=True)

