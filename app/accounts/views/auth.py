from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.auth import RequestPhoneSerializer, VerifyCodeSerializer, TokenPairSerializer
from accounts.services.auth import send_verification_code, verify_code, generate_tokens_for_user


@extend_schema(
    summary="Запрос кода авторизации",
    description="Отправляет 4-значный код (имитация) на указанный номер телефона. Код действует 5 минут.",
    request=RequestPhoneSerializer,
    responses={200: OpenApiResponse(description="Код успешно отправлен")}
)
class RequestCodeView(APIView):
    def post(self, request: Request) -> Response:
        serializer = RequestPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone: str = serializer.validated_data["phone"]
        send_verification_code(phone)
        return Response({"detail": "Код отправлен"}, status=status.HTTP_200_OK)


@extend_schema(
    summary="Подтверждение кода и выдача JWT",
    description="Проверяет введённый код. Если код верный — создаёт пользователя (если новый) и выдаёт access/refresh токены.",
    request=VerifyCodeSerializer,
    responses={200: TokenPairSerializer}
)
class VerifyCodeView(APIView):
    def post(self, request: Request) -> Response:
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone: str = serializer.validated_data["phone"]
        code: str = serializer.validated_data["code"]

        user = verify_code(phone, code)
        if not user:
            return Response({"detail": "Неверный или просроченный код"}, status=status.HTTP_400_BAD_REQUEST)

        tokens: dict[str, str] = generate_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)
