from typing import Any

from rest_framework import serializers

from accounts.models import User


class InvitedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone"]


class UserProfileSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["phone", "invite_code", "used_invite_code", "invited_users"]

    def get_invited_users(self, obj) -> list[dict[str, Any]]:
        if not obj.invite_code:
            return []
        users = User.objects.filter(used_invite_code=obj.invite_code)
        return InvitedUserSerializer(users, many=True).data


class ActivateInviteCodeSerializer(serializers.Serializer):
    access = serializers.CharField()
    code = serializers.CharField(max_length=6)
