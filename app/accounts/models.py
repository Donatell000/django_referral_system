from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, phone):
        if not phone:
            raise ValueError("Введите номер телефона")
        user = self.model(phone=phone)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        if not password:
            raise ValueError("Суперпользователь должен иметь пароль")
        user = self.model(phone=phone)
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="Номер телефона",
    )
    invite_code = models.CharField(
        max_length=6,
        unique=True,
        blank=True,
        null=True,
        default=None,
        verbose_name="invite-код",
    )
    used_invite_code = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        verbose_name="Использованный invite-код",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Сотрудник",
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
