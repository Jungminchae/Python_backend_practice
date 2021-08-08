from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class RegisgerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=68, min_length=6)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, validated_data):
        username = validated_data.get("username", "")
        email = validated_data.get("email", "")

        if not username.isalnum():
            raise serializers.ValidationError("username은 알파벳or숫자 가능합니다")

        return validated_data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=500)

    class Meta:
        model = User
        fields = ["token"]


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=3, write_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "username", "tokens")
        read_only_fields = ("username",)

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid Credentials")

        if not user.is_active:
            raise AuthenticationFailed("Account disabled")

        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        return {"email": user.email, "username": user.username, "tokens": user.tokens()}
