from rest_framework import serializers
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
