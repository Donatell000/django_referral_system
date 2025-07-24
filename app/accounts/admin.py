from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "phone",
        "invite_code",
        "used_invite_code",
        "invited_users",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("phone", "invite_code", "used_invite_code")
    readonly_fields = ("invited_users",)

    def invited_users(self, obj):
        if not obj.invite_code:
            return "—"
        phones = User.objects.filter(used_invite_code=obj.invite_code).values_list("phone", flat=True)
        return ", ".join(phones) if phones else "—"

    invited_users.short_description = "Приглашенные пользователи"


admin.site.unregister(Group)
