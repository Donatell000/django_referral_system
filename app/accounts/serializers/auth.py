import re

from rest_framework import serializers


class PhoneValidationMixin:
    def validate_phone(self, value: str) -> str:
        if not re.fullmatch(r"\+7\d{10}", value):
            raise serializers.ValidationError("Введите номер в формате +7XXXXXXXXXX")
        return value


class RequestPhoneSerializer(PhoneValidationMixin, serializers.Serializer):
    phone = serializers.CharField(max_length=15)


class VerifyCodeSerializer(PhoneValidationMixin, serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=4)

    def validate_code(self, value: str) -> str:
        if not re.fullmatch(r"\d{4}", value):
            raise serializers.ValidationError("Код должен состоять из 4 цифр")
        return value


class TokenPairSerializer(serializers.Serializer):
    access = serializers.CharField(help_text="JWT access-токен")
    refresh = serializers.CharField(help_text="JWT refresh-токен")
