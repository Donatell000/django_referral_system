import random
import string
from time import sleep

from django.core.cache import cache
from django.db import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


def generate_verification_code() -> str:
    return str(random.randint(1000, 9999))


def send_verification_code(phone: str) -> str:
    code = generate_verification_code()
    cache.set(f"verify_code:{phone}", code, timeout=300)
    sleep(1.5)
    print(f"[DEBUG] Код для {phone}: {code}")
    return code


def verify_code(phone: str, code: str) -> User | None:
    cached_code = cache.get(f"verify_code:{phone}")
    if not cached_code or cached_code != code:
        return None
    cache.delete(f"verify_code:{phone}")

    try:
        user = User.objects.get(phone=phone)
        return user
    except User.DoesNotExist:
        pass

    characters = string.ascii_letters + string.digits
    for _ in range(10):
        invite_code = "".join(random.choices(characters, k=6))
        user = User(phone=phone, invite_code=invite_code)
        try:
            user.save()
            return user
        except IntegrityError:
            continue

    raise Exception("Не удалось сгенерировать уникальный invite_code после 10 попыток")


def generate_tokens_for_user(user: User) -> dict[str, str]:
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
