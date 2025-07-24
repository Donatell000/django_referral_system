from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers.profile import UserProfileSerializer, ActivateInviteCodeSerializer
from accounts.services.profile import activate_invite_code


@extend_schema(
    summary="Получить профиль пользователя",
    description="Возвращает номер телефона, собственный invite-код, чей invite-код был использован, и список приглашённых пользователей.",
    request=None,
    responses={200: UserProfileSerializer}
)
class UserProfileView(APIView):
    def post(self, request: Request) -> Response:
        token_str: str | None = request.data.get("access")
        if not token_str:
            return Response({"detail": "Неправильный токен"},status=status.HTTP_400_BAD_REQUEST)

        try:
            token: AccessToken = AccessToken(token_str)
            user: User = User.objects.get(id=token["user_id"])
        except Exception:
            return Response({"detail": "Недействительный или просроченный токен"},status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Активировать чужой invite-код",
    description="Позволяет ввести чужой инвайт-код. Можно активировать только один раз.",
    request=ActivateInviteCodeSerializer,
    responses={200: OpenApiResponse(description="Invite-код активирован")}
)
class ActivateInviteCodeView(APIView):
    def post(self, request: Request) -> Response:
        serializer = ActivateInviteCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access: str = serializer.validated_data["access"]
        code: str = serializer.validated_data["code"]

        user, error = activate_invite_code(access, code)
        if error:
            return Response({"detail": error},status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Invite-код активирован"},status=status.HTTP_200_OK)
