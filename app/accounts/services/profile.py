from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User


def activate_invite_code(access: str, code: str) -> tuple[User | None, str | None]:
    try:
        token = AccessToken(access)
        user = User.objects.get(id=token["user_id"])
    except Exception:
        return None, "Неправильный токен"

    if user.used_invite_code:
        return None, "Invite-код уже использован"

    try:
        inviter = User.objects.get(invite_code=code)
    except User.DoesNotExist:
        return None, "Неправильный invite-код"

    if inviter.id == user.id:
        return None, "Невозможно использовать свой собственный invite-код"

    user.used_invite_code = code
    user.save()
    return user, None
